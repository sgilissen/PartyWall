# ---------------------------------------------------------
# MODULE IMPORTS
# ---------------------------------------------------------
from typing import Optional, Awaitable
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.escape
import threading
import json
import os

# ---------------------------------------------------------
# VARIABLES
# ---------------------------------------------------------
root = os.path.dirname(os.path.realpath(__file__))
web_root = os.path.join(root, "html/")
ws_clients = []

settings = {
    "static_path": os.path.join(web_root, "static/"),
    "template_path": web_root,
    "xsrf_cookies": False,
}


class HomeHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.render("redir.html")


class MainHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.render("main.html")


class MobileHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.render("mobile.html")

    def post(self):
        msg = self.request.body.decode('utf-8')
        print(f"Received message: {msg}")
        if msg is not "":
            self.write("Bericht ontvangen!")
            write_to_client_ws(msg)
        else:
            self.write("Geef je bericht op in het tekstvak.")




class SocketHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in ws_clients:
            ws_clients.append(self)

    def on_message(self, message):
        msg_json = json.loads(message)

        msg_dict = {
            "msg_type": msg_json['msg_type'],
            "src_ip": self.request.remote_ip,
            "src_host": self.request.host_name,
            "payload": msg_json['payload']
        }


# ---------------------------------------------------------
# Main thread class
# ---------------------------------------------------------
class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__(daemon=True)
        self.__stop_event = threading.Event()

    def run(self):
        pass

    def stop(self):
        self.__stop_event.set()

    def stopped(self):
        return self.__stop_event.is_set()


# ---------------------------------------------------------
# Functions
# ---------------------------------------------------------
def write_to_client_ws(message):
    for c in ws_clients:
        c.write_message(message)


if __name__ == '__main__':
    print(web_root)
    print(settings.get('static_path'))
    app = tornado.web.Application([
        ("/", HomeHandler),
        ("/_wall", MainHandler),
        ("/chat", MobileHandler),
        ("/ws", SocketHandler),
    ], **settings)

    app.listen(8999)
    tornado.ioloop.IOLoop.current().start()
