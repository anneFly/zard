import os
import json

import tornado.ioloop
import tornado.web
import sockjs.tornado

from webgame import game, exceptions


global_game = game.Game()
users = set()

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
STATICS_DIR = os.path.join(PROJECT_DIR, 'statics')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        template_name = os.path.join(PROJECT_DIR, 'templates/zard.html')
        self.render(template_name)


class GameConnection(sockjs.tornado.SockJSConnection):
    _next_id = 1

    def on_open(self, info):
        users.add(self)

    def on_close(self):
        users.remove(self)

    def on_message(self, msg):
        message = json.loads(msg)

        if message[0] == 'start':
            name = 'player_{}'.format(type(self)._next_id)
            type(self)._next_id += 1

            global_game.add_user(self, name)
            if global_game.num_players == 3:
                global_game.start()

        elif message[0] == 'guess':
            guess = message[1]
            try:
                global_game.on_guess(self, guess)
            except exceptions.GameException as e:
                self.broadcast([self], json.dumps(['error', str(e)]))

        elif message[0] == 'play':
            card_id = message[1]
            try:
                global_game.on_play_card(self, card_id)
            except exceptions.GameException as e:
                self.broadcast([self], json.dumps(['error', str(e)]))


game_router = sockjs.tornado.SockJSRouter(GameConnection, '/sock')

app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/statics/(.*)', tornado.web.StaticFileHandler, {'path': STATICS_DIR}),
] + game_router.urls, debug=True)

if __name__ == "__main__":
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
