#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa
import sys
import os
import os.path
import re
import zipfile

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

    username = sys.argv[1]
    tmpdir = os.path.join(os.getcwd(), 'tmp')
    userdir = os.path.join(tmpdir, username)
    if len(sys.argv) == 3: 


    if not os.path.isdir(userdir):
        os.makedirs(userdir)

    zf = zipfile.ZipFile(os.path.join(userdir, username+'_search.zip'), 'r')
    for f in zf.namelist():
        encfile = zf.read(f)
        f = f.split('.')
        content = dec(encfile)
        with open(os.path.join(userdir, f[0]), 'w+') as outputfile:
            outputfile.write(content)
            outputfile.close()
