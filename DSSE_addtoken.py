#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa
import sys
import os
import os.path
import re
import hashlib
import random
import pickle

enc_pattern = re.compile(r'.*\.enc')
dec_pattern = re.compile(r'.*\.dec')
pickle_pattern = re.compile(r'.*\.pickle')

keywords_set = []

def CalcSha1(word):
    sha1obj = hashlib.sha1()
    sha1obj.update(word)
    hash = sha1obj.hexdigest()
    return hash

def CalcMD5(word):
    md5obj = hashlib.md5()
    md5obj.update(word)
    hash = md5obj.hexdigest()
    return hash

def DSSE_addtoken(username, parent, filename):
    file_path = os.path.join(parent, filename)

    print '-----------------DSSE_add------------------\n'
    with open(file_path) as inputfile:
        raw_content = inputfile.read()
    
    spli = raw_content.split()
    keywords = list(set(spli))
    tmpdir = os.path.join(os.getcwd(), 'tmp/'+username)
    with open(os.path.join(tmpdir, 'add_token.tmp'), 'w+') as outputfile:
        outputfile.write(filename+'\n')
        for word in keywords:
            outputfile.write(word+'\n')

if __name__ == '__main__':
    print 'argv[0]: ', sys.argv[0]
    print 'argv[1]: ', sys.argv[1]
    print 'argv[2]: ', sys.argv[2]
    rootdir = os.path.join(os.getcwd(), sys.argv[1])
    print rootdir

    parent = rootdir
    filename = sys.argv[2]

    if not ( enc_pattern.match(filename)
          or dec_pattern.match(filename)
          or pickle_pattern.match(filename) ):
          DSSE_addtoken(sys.argv[1], parent, filename)
