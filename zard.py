import json
import os
import random
import time

import tornado.ioloop
import tornado.web
from sockjs.tornado import SockJSRouter, SockJSConnection

from webgame.game import Game
from webgame.exceptions import GameException


users = set()
games = {}

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
STATICS_DIR = os.path.join(PROJECT_DIR, 'statics')


def serialize_lobby_status():
    return json.dumps([
        'lobby',
        {
            'users': [u.name for u in users if u.name],
            'games': [
                {
                    'id': game_id,
                    'name': game.name,
                    'size': game.size,
                    'status': game.state,
                    'users': [u.name for u in game.users],
                }
                for game_id, game in games.items()
            ]
        }
    ])


def serialize_user_status(user):
    return json.dumps([
        'userState',
        {
            'userName': user.name,
            'inGame': bool(user.game),
        }
    ])


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        template_name = os.path.join(PROJECT_DIR, 'templates/zard.html')
        self.render(template_name)


class GameConnection(SockJSConnection):
    message_handlers = {
        'rename': 'rename',
        'createGame': 'create_game',
        'joinGame': 'join_game',
        'leaveGame': 'leave_game',
        'guess': 'guess',
        'play': 'play',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = None

    def on_open(self, info):
        self.id = str(str(time.time()) + str(info.ip))\
            .replace('.', '')\
            .replace(':', '')
        self.name = ''
        users.add(self)
        self.send(serialize_user_status(self))
        self.broadcast(users, serialize_lobby_status())

    def on_close(self):
        self.leave_game()
        users.remove(self)
        self.broadcast(users, serialize_lobby_status())

    def on_message(self, msg):
        try:
            message = json.loads(msg)
        except (ValueError, TypeError):
            self.send(json.dumps(['error', {'msg': 'Invalid JSON!'}]))
            return

        try:
            command = message[0]
        except IndexError:
            self.send(json.dumps(['error', {'msg': 'No command specified!'}]))
            return

        kwargs = message[1] if len(message) > 1 else {}

        try:
            handler = self.message_handlers[command]
            getattr(self, handler)(**kwargs)
        except KeyError:
            self.send(json.dumps(['error', {'msg': 'Invalid command!'}]))
        except GameException as e:
            self.send(json.dumps(['error', {'msg': str(e.message)}]))

    def rename(self, **kwargs):
        name = kwargs.get('name')

        if not name:
            raise GameException('You must provide a name.')

        if len(name) < 3:
            raise GameException('The name is too short (min 3 characters).')

        if len(name) > 35:
            raise GameException('The name is too long (max 35 characters).')

        self.name = name

        self.send(serialize_user_status(self))
        self.broadcast(users, serialize_lobby_status())

    def create_game(self, **kwargs):
        name = kwargs.get('name')
        size = kwargs.get('size')

        if not name:
            raise GameException('You must provide a name for your game.')

        if not size:
            raise GameException('You must provide a size for your game.')

        if len(name) < 3:
            raise GameException('The game name is too short (min 3 '
                                'characters).')

        if len(name) > 35:
            raise GameException('The game name is too long (max 35 '
                                'characters).')

        try:
            int(size)
        except ValueError:
            raise GameException('This is not a valid amount of players.')

        if not size or int(size) < 3 or int(size) > 6:
            raise GameException('The game size must be between 3 and 6.')

        if self.game is not None:
            raise GameException('You already joined a game. Leave your current'
                                ' game to create a new one.')

        game = Game(name, int(size))
        game.add_user(self)
        self.game = game
        games[game.id] = game

        self.send(serialize_user_status(self))
        self.broadcast(users, serialize_lobby_status())

    def join_game(self, **kwargs):
        id = kwargs.get('id')

        if not id:
            raise GameException('No game id was provided.')

        if self.game is not None:
            raise GameException('You already joined a game. Leave your current'
                                ' game to join a new one.')
        try:
            game = games[id]
        except KeyError:
            raise GameException('Unable to find the game.')

        game.add_user(self)
        self.game = game

        self.send(serialize_user_status(self))
        self.broadcast(users, serialize_lobby_status())

    def leave_game(self, **kwargs):
        if self.game:
            self.game.remove_user(self)

            if len(self.game.users) == 0:
                games.pop(self.game.id)

            self.game = None

        self.send(serialize_user_status(self))
        self.broadcast(users, serialize_lobby_status())

    def guess(self, **kwargs):
        guess = kwargs.get('guess')

        if guess in [None, '']:
            raise GameException('You have to make a guess.')

        try:
            int(guess)
        except ValueError:
            raise GameException('This is not a valid guess.')

        if int(guess) < 0:
            raise GameException('Your guess cannot be a negative number.')

        if self.game:
            self.game.on_guess(self, int(guess))

    def play(self, **kwargs):
        card_id = kwargs.get('card')

        if not card_id:
            raise GameException('No card id provided.')

        if self.game:
            self.game.on_play_card(self, card_id)


game_router = SockJSRouter(GameConnection, '/sock')

app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/statics/(.*)', tornado.web.StaticFileHandler, {'path': STATICS_DIR}),
] + game_router.urls, debug=True)

if __name__ == "__main__":
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
