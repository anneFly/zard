import os
import json
import html

import tornado.ioloop
import tornado.web
import sockjs.tornado


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
STATICS_DIR = os.path.join(PROJECT_DIR, "statics")

_player_id = 1
participants = set()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        template_name = os.path.join(PROJECT_DIR, "templates/index.html")
        self.render(template_name, title="ZARD!")


class GameConnection(sockjs.tornado.SockJSConnection):
    def on_open(self, info):
        global _player_id
        self.name = ""
        _player_id += 1
        participants.add(self)
        self.broadcast_player_names()

    def on_close(self):
        participants.remove(self)
        self.broadcast_player_names()

    def on_message(self, msg):
        message = json.loads(msg)
        if message[0] == "chatmessage":
            self.broadcast(participants, json.dumps([
                "chatmessage",
                self.name,
                html.escape(message[1])
            ]))
        elif message[0] == "playername":
            self.name = message[1]
            self.broadcast_player_names()

    def broadcast_player_names(self):
        names = [html.escape(p.name) for p in participants]
        self.broadcast(participants, json.dumps(["players", names]))


game_router = sockjs.tornado.SockJSRouter(GameConnection, '/sock')

app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/statics/(.*)", tornado.web.StaticFileHandler, {"path": STATICS_DIR}),
] + game_router.urls, debug=True)

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
