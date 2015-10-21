import json
import os
import time

import tornado.ioloop
import tornado.web
import sockjs.tornado

from webgame.game import Game
from webgame.exceptions import GameException


users = set()
games = {}

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
STATICS_DIR = os.path.join(PROJECT_DIR, 'statics')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        template_name = os.path.join(PROJECT_DIR, 'templates/zard.html')
        self.render(template_name)


class GameConnection(sockjs.tornado.SockJSConnection):
    id = None
    name = ''
    game = None

    def on_open(self, info):
        self.id = str(str(time.time()) + str(info.ip)).replace('.', '').replace(':', '')
        users.add(self)

    def on_close(self):
        self.leave_game()
        users.remove(self)

    def on_message(self, msg):
        message = json.loads(msg)

        try:
            if message[0] == 'rename':
                self.rename(*message[1:])

            elif message[0] == 'createGame':
                self.create_game(*message[1:])

            elif message[0] == 'joinGame':
                self.join_game(*message[1:])

            elif message[0] == 'leaveGame':
                self.leave_game(*message[1:])

            elif message[0] == 'guess':
                self.guess(*message[1:])

            elif message[0] == 'play':
                self.play(*message[1:])
        except GameException as e:
            self.broadcast([self], json.dumps(['error', str(e.message)]))

    def rename(self, name, *args):
        if not name:
            raise GameException('You must provide a name.')
        self.name = name

    def create_game(self, game_name, size, *args):
        if not game_name:
            raise GameException('You must provide a name for your game.')

        if not size or int(size) < 3 or int(size) > 6:
            raise GameException('The game size must be between 3 and 6.')

        if self.game is not None:
            raise GameException('You already joined a game. Leave your current game '
                                'to create a new one.')

        game = Game(game_name, int(size))
        game.add_user(self)
        self.game = game
        games[game.id] = game

    def join_game(self, game_id, *args):
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

    def leave_game(self, *args):
        if self.game:
            self.game.remove_user(self)

    def guess(self, guess, *args):
        if guess in [None, '']:
            raise GameException('You have to make a guess.')

        try:
            int(guess)
        except ValueError:
            raise GameException('This is not a valid guess.')

        if self.game:
            self.game.on_guess(self, guess)

    def play(self, card_id, *args):
        if not card_id:
            raise GameException('No card id provided.')

        if self.game:
            self.game.on_play_card(self, card_id)


game_router = sockjs.tornado.SockJSRouter(GameConnection, '/sock')

app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/statics/(.*)', tornado.web.StaticFileHandler, {'path': STATICS_DIR}),
] + game_router.urls, debug=True)

if __name__ == "__main__":
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
