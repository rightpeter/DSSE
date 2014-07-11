#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa

def gen():
    (pubkey, privkey) = rsa.newkeys(2048)
    
    print 'pubkey: ', pubkey
    print 'privkey: ', privkey

    pub = pubkey.save_pkcs1()
    pubfile = open('public.pem', 'w+')
    pubfile.write(pub)
    pubfile.close()
    
    pri = privkey.save_pkcs1()
    prifile = open('private.pem', 'w+')
    prifile.write(pri)
    prifile.close()
    
if __name__ == '__main__':
    gen()
