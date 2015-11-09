import time
import random
import multiprocessing
import contextlib

from websocket import create_connection
import tornado.ioloop

import zard


@contextlib.contextmanager
def run_server(port):
    def _server(port):
        zard.app.listen(port)
        tornado.ioloop.IOLoop.instance().start()

    proc = multiprocessing.Process(target=_server, args=(port, ))
    proc.start()
    time.sleep(1) # let the server warm up
    yield
    proc.terminate()

def test_gameplay():
    """Test gameplay using real connections"""
    port = random.randint(9000, 14000)
    address = "ws://localhost:{}/sock/websocket".format(port)

    with run_server(port):
        # spawn 3 clients
        c1 = create_connection(address)
        c2 = create_connection(address)
        c3 = create_connection(address)

        c1.send("hi")
        print(c1.recv())


if __name__ == "__main__":
    test_gameplay()
