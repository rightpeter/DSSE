#!/usr/bin/python
# encoding: utf-8

import tornado.web
import tornado.ioloop
import os.path
import pickle
import json
from DSSE_search import *
from DSSE_add import *
from DSSE_del import *
from myTool import *

from tornado.options import define, options

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


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WorkHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("work.html")


class AddHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("add.html")

    def post(self):
        username = self.get_argument('username')
        add_token = self.request.files['myfile'][0]['body']
        add_token = add_token.split()
        enc_file = self.request.files['myfile'][1]
        DSSE_add(username, add_token, enc_file)
        self.write('Add Successfully!')


class DeleteHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("delete.html")

    def post(self):
        username = self.get_argument('username')
        filename = self.get_argument('filename')

        DSSE_del(username, filename)
        self.write('Delete Successfully!')


class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("search.html")

    def post(self):
        username = self.get_argument('username')
        word = self.get_argument('word')
        self.set_header('Content-Type', 'application-zip')
        self.set_header('Content-Disposition', 'attachment;filename=%s_search.zip' % CalcSha1(word))
        file_list = DSSE_search(username, CalcSha1(word), int(CalcMD5(word), 16))
        tmpdir = os.path.join(os.getcwd(), 'static/tmp/' + username)
        with open(os.path.join(tmpdir, CalcSha1(word) + '_search.zip'), 'r') as inputfile:
            content = inputfile.read()
            self.write(content)


class SearchFileHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('username')
        srchtoken = self.request.files['myfile'][0]['body']
        print self.request.files['myfile'][0]['filename']
        srchtoken = srchtoken.split()
        file_list = DSSE_search(username, srchtoken[1], int(srchtoken[2], 16))
        print file_list
        self.write(str(file_list))


class TextFullHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("text_full.html")


class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload.html")

    def post(self):
        username = self.get_argument('username')
        rootdir = os.getcwd()
        parent = os.path.join(rootdir, 'static/db/' + username)
        print parent
        if not os.path.isdir(parent):
            print 'mkdir'
            os.makedirs(parent)
        else:
            self.write('Username Already Exist!')
            return

        if self.request.files:
            upload_file = self.request.files['myfile'][0]
            with open(parent + '/zipfile.zip', 'w') as uploadfile:
                uploadfile.write(upload_file['body'])

            zf = zipfile.ZipFile(os.path.join(parent, 'zipfile.zip'), 'r')
            zf.extractall(parent, zf.namelist())
            zf.close()

        self.write('Upload Successful!')


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application-zip')
        self.set_header('Content-Disposition', 'attachment;filename=search.zip')
        rootdir = os.getcwd()
        parent = os.path.join(rootdir, 'static/db/haha/zipfile.zip')
        print parent
        with open(parent, 'r') as inputfile:
            input = inputfile.read()
            self.write(input)


def main():
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
