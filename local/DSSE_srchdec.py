#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa
import sys
import os
import re
import zipfile
import myTools
import traceback

enc_pattern = re.compile(r'.*\.enc$')
dec_pattern = re.compile(r'.*\.dec$')


def DSSE_dec(crypto):
    with open('public.pem') as publickfile:
        p = publickfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)

    with open('private.pem') as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)

    content = ''
    while crypto:
        enc_message = crypto[:256]
        crypto = crypto[256:]

        message = rsa.decrypt(enc_message, privkey)
        content += message
        print '-----------------message: -------------\n', message
        print '-----------------content: -------------\n', content
        # print '-----------------enc_message: ---------\n', enc_message.decode('utf-8')
        # print '-----------------crypto: --------------\n', crypto

    # content = rsa.decrypt(crypto, privkey)
    print 'content: ', content

    return content

def srchdec(username, word):
    tmpdir = os.path.join(os.getcwd(), 'tmp', username)
    userdir = os.path.join(os.getcwd(), 'db', username, word)

    if os.path.isdir(userdir):
        for parent, dirnames, filenames in os.walk(userdir):
            for filename in filenames:
                os.remove(os.path.join(parent, filename))
    else:
        os.makedirs(userdir)

    try:
        word_sha1 = myTools.CalcSha1(word)
        zf = zipfile.ZipFile(os.path.join(tmpdir, word_sha1 + '_search.zip'), 'r')
        for f in zf.namelist():
            if enc_pattern.match(f):
                encfile = zf.read(f)
                f = f.split('.')
                content = DSSE_dec(encfile)
                with open(os.path.join(userdir, f[0]), 'w+') as outputfile:
                    outputfile.write(content)
                    outputfile.close()
        os.remove(os.path.join(tmpdir, word_sha1 + '_search.zip'))
    except Exception, e:
        print traceback.print_exc()
        print 'No Folder!'


if __name__ == '__main__':
    username = sys.argv[1]
    word = sys.argv[2]

    srchdec(username, word)
