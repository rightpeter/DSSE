#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class WorkHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("work.html")


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
