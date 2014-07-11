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

if __name__ == '__main__':
    #print 'argv[0]: ', sys.argv[0]
    #print 'argv[1]: ', sys.argv[1]
    #print 'argv[2]: ', sys.argv[2]

    username = sys.argv[1]
    word = sys.argv[2]

    print username, ' ', CalcSha1(word)
    with open('srch_token.tmp', 'w+') as outputfile:
        outputfile.write(username+' '+CalcSha1(word)+' '+CalcMD5(word))
        
