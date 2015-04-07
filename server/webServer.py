#!/usr/bin/python
# encoding: utf-8

import tornado.web
import tornado.ioloop
import os.path
import pickle
import json

from tornado.options import define, options
from controller.dsseHandlers import AddHandler, DeleteHandler, SearchHandler, SearchFileHandler
from controller.webHandlers import MainHandler, WorkHandler, TextFullHandler, UploadHandler, TestHandler

define("port", default=8089, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/work', WorkHandler),
            (r'/add', AddHandler),
            (r'/delete', DeleteHandler),
            (r'/search', SearchHandler),
            (r'/searchfile', SearchFileHandler),
            (r'/text_full', TextFullHandler),
            (r'/upload', UploadHandler),
            (r'/test1', TestHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
