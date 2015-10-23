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
            'numUsers': len(users),
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


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        template_name = os.path.join(PROJECT_DIR, 'templates/zard.html')
        self.render(template_name)


class GameConnection(SockJSConnection):
    id = None
    name = ''
    game = None

    def on_open(self, info):
        self.id = str(str(time.time()) + str(info.ip)).replace('.', '').replace(':', '')
        self.name = 'player_{}'.format(random.randint(10000, 99999))
        users.add(self)
        self.broadcast(users, serialize_lobby_status())

    def on_close(self):
        self.leave_game()
        users.remove(self)
        self.broadcast(users, serialize_lobby_status())

    def on_message(self, msg):
        message = json.loads(msg)
        code = message[0]
        args = message[1:]

        try:
            if code == 'rename':
                self.rename(*args)

            elif code == 'createGame':
                self.create_game(*args)

            elif code == 'joinGame':
                self.join_game(*args)

            elif code == 'leaveGame':
                self.leave_game(*args)

            elif code == 'guess':
                self.guess(*args)

            elif code == 'play':
                self.play(*args)

        except GameException as e:
            self.send(json.dumps(['error', str(e.message)]))

    def rename(self, *args):
        try:
            name, = args
        except ValueError:
            raise GameException('You must provide a name.')

        if not name:
            raise GameException('You must provide a name.')

        if len(name) < 3:
            raise GameException('The name is too short (min 3 characters).')

        if len(name) > 35:
            raise GameException('The name is too long (max 35 characters).')

        self.name = name

        self.broadcast(users, serialize_lobby_status())

    def create_game(self, *args):
        try:
            game_name, size = args
        except ValueError:
            raise GameException('You must provide a name and a size for your game.')

        if not game_name:
            raise GameException('You must provide a name for your game.')

        if len(game_name) < 3:
            raise GameException('The game name is too short (min 3 characters).')

        if len(game_name) > 35:
            raise GameException('The game name is too long (max 35 characters).')

        if not size or int(size) < 3 or int(size) > 6:
            raise GameException('The game size must be between 3 and 6.')

        if self.game is not None:
            raise GameException('You already joined a game. Leave your current game '
                                'to create a new one.')

        game = Game(game_name, int(size))
        game.add_user(self)
        self.game = game
        games[game.id] = game

        self.broadcast(users, serialize_lobby_status())

    def join_game(self, *args):
        try:
            game_id, = args
        except ValueError:
            raise GameException('No game id was provided.')

        if not game_id:
            raise GameException('No game id was provided.')

        if self.game is not None:
            raise GameException('You already joined a game. Leave your current game '
                                'to join a new one.')
        try:
            game = games[game_id]
        except KeyError:
            raise GameException('Unable to find the game.')

        game.add_user(self)
        self.game = game

        self.broadcast(users, serialize_lobby_status())

    def leave_game(self, *args):
        if self.game:
            self.game.remove_user(self)
        if len(self.game.users) == 0:
            games.pop(self.game.id)
        self.game = None

        self.broadcast(users, serialize_lobby_status())

    def guess(self, *args):
        try:
            guess, = args
        except ValueError:
            raise GameException('You have to make a guess.')

        if guess in [None, '']:
            raise GameException('You have to make a guess.')

        try:
            int(guess)
        except ValueError:
            raise GameException('This is not a valid guess.')

        if self.game:
            self.game.on_guess(self, guess)

    def play(self, *args):
        try:
            card_id, = args
        except ValueError:
            raise GameException('No card id provided.')

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
