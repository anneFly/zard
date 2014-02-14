import os

import tornado.ioloop
import tornado.web
import sockjs.tornado


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
STATICS_DIR = os.path.join(PROJECT_DIR, 'statics')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        template_name = os.path.join(PROJECT_DIR, "templates/index.html")
        self.render(template_name, title="ZARD!")


class GameConnection(sockjs.tornado.SockJSConnection):
    def on_message(self, msg):
        self.send("--> {}".format(msg))

game_router = sockjs.tornado.SockJSRouter(GameConnection, '/sock')

app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/statics/(.*)", tornado.web.StaticFileHandler, {"path": STATICS_DIR}),
] + game_router.urls, debug=True)

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
