#!/usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.web

class Navbar(tornado.web.UIModule):
    def render(self, brand, navs, user):
        return self.render_string("navbar.html", brand=brand, navs=navs, user=user)

class NavbarDSSE(Navbar):
    def render(self, user, url):
        brand = {}
        brand['href'] = '/'
        brand['name'] = 'DSSE Cloud Service'

        navs = [{}, {}]
        navs[0]['name'] = 'Guide'
        navs[0]['href'] = '/'
        navs[1]['name'] = 'Actions'
        navs[1]['href'] = '/dsse'

        if url == '/':
            navs[0]['active'] = True
        elif url == '/dsse':
            navs[1]['active'] = True
    
        name = {}

        return Navbar.render(self, brand, navs, user) 
