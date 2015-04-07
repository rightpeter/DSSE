#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
from operation.dsseCore import DSSE_add, DSSE_del, DSSE_search


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
