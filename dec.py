#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa
import sys
import os
import os.path
import re

enc_pattern = re.compile(r'.*\.enc$')
dec_pattern = re.compile(r'.*\.dec$')

def enc(file_path):
    with open(file_path) as inputfile:
        crypto = inputfile.read()
    
    print crypto
    with open('public.pem') as publickfile:
        p = publickfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)
    
    with open('private.pem') as privatefile:
        p = privatefile.read()
        privkey= rsa.PrivateKey.load_pkcs1(p)
    
    content = ''
    while crypto:
        enc_message = crypto[:256]
        crypto = crypto[256:]

        message = rsa.decrypt(enc_message, privkey)
        content += message
        print '-----------------message: -------------\n', message
        print '-----------------content: -------------\n', content
        print '-----------------enc_message: ---------\n', enc_message
        print '-----------------crypto: --------------\n', crypto

    #content = rsa.decrypt(crypto, privkey)
    print 'content: ', content

    with open(file_path+'.dec', 'w+') as outputfile:
        outputfile.write(content)
        outputfile.close()
        
if __name__ == '__main__':
    print 'argv[0]: ', sys.argv[0]
    print 'argv[1]: ', sys.argv[1]
    rootdir = os.path.join(os.getcwd(), sys.argv[1])
    print rootdir
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            print "parent is:" + parent
            print "filename is:" + filename
            file_path = os.path.join(parent, filename)
            print "the full name of the file is:" + file_path
            if enc_pattern.match(file_path):
                enc(file_path)
