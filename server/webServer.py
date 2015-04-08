#!/usr/bin/python
# encoding: utf-8

import tornado.web
import tornado.ioloop
import os.path
import pickle
import json
import util.uimodules as uimodules

from tornado.options import define, options
from controller.dsseHandlers import AddHandler, DeleteHandler, SearchHandler, SearchFileHandler
from controller.webHandlers import MainHandler, UploadHandler, TestHandler, DownloadHandler, DSSEHandler

define("port", default=8090, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/dsse', DSSEHandler),
            (r'/download', DownloadHandler),
            (r'/add', AddHandler),
            (r'/delete', DeleteHandler),
            (r'/search', SearchHandler),
            (r'/searchfile', SearchFileHandler),
            (r'/upload', UploadHandler),
            (r'/test1', TestHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules=uimodules,
            cookie_secret="#De1rFq@oyW^!kc3MI@74LY*^TPG6J8fkiG@xidDBF",
            login_url="/login",
            xsrf_cookies=True,
            debug=True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
