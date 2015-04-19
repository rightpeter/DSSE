#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import os
import zipfile


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("name")

    def get_login_url(self):
        return '/login'


class MainHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        self.set_cookie('url', self.request.uri)
        url = self.request.uri

        self.render("index.html", user=user, url=url)


class DSSEHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        self.set_cookie('url', self.request.uri)
        url = self.request.uri
        content = self.get_argument('action', 'upload')

        self.render('dsse.html', user=user, url=url, content=content)


class DownloadHandler(BaseHandler):
    def get(self):
        self.redirect('/static/download/client.zip')


class UploadHandler(BaseHandler):
    def post(self):
        print 'hehe'
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


class TestHandler(BaseHandler):
    def get(self):
        self.set_header('Content-Type', 'application-zip')
        self.set_header('Content-Disposition', 'attachment;filename=search.zip')
        rootdir = os.getcwd()
        parent = os.path.join(rootdir, 'static/db/haha/zipfile.zip')
        print parent
        with open(parent, 'r') as inputfile:
            input = inputfile.read()
            self.write(input)
