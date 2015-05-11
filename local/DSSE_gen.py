#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa
import os

def gen(path):
    (pubkey, privkey) = rsa.newkeys(2048)
    
    print 'pubkey: ', pubkey
    print 'privkey: ', privkey

    pub = pubkey.save_pkcs1()
    public_file = os.path.join(path, 'public.pem')
    pubfile = open(public_file, 'w+')
    pubfile.write(pub)
    pubfile.close()
    
    pri = privkey.save_pkcs1()
    private_file = os.path.join(path, 'private.pem')
    prifile = open(private_file, 'w+')
    prifile.write(pri)
    prifile.close()

    return True
    
if __name__ == '__main__':
    gen()
