#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa
import sys
import os
import os.path
import re
import zipfile
from myTool import *

enc_pattern = re.compile(r'.*\.enc$')
dec_pattern = re.compile(r'.*\.dec$')

def dec(crypto):
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

    return content
        
if __name__ == '__main__':
    print 'argv[0]: ', sys.argv[0]
    print 'argv[1]: ', sys.argv[1]
    print 'argv[2]: ', sys.argv[2]

    username = sys.argv[1]
    word = sys.argv[2]
    tmpdir = os.path.join(os.getcwd(), 'tmp', username)
    userdir = os.path.join(os.getcwd(), 'db', username, word)

    if os.path.isdir(userdir):
        for parent, dirnames, filenames in os.walk(userdir):
            for filename in filenames:
                os.remove(os.path.join(parent, filename))
    else:
        os.makedirs(userdir)

    try:
        word_sha1 = CalcSha1(word) 
        zf = zipfile.ZipFile(os.path.join(tmpdir, word_sha1+'_search.zip'), 'r')
        for f in zf.namelist():
            if enc_pattern.match(f):
                encfile = zf.read(f)
                f = f.split('.')
                content = dec(encfile)
                with open(os.path.join(userdir, f[0]), 'w+') as outputfile:
                    outputfile.write(content)
                    outputfile.close()
        os.remove(os.path.join(tmpdir, word_sha1+'_search.zip'))
    except Exception, e:
        print e
        print 'No Folder!'