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
    print 'argv[0]: ', sys.argv[0]
    print 'argv[1]: ', sys.argv[1]
    rootdir = os.path.join(os.getcwd(), sys.argv[1])
    print rootdir

    print os.path.join(rootdir, 'TS.pickle')
    with open(os.path.join(rootdir, 'TS.pickle'), 'r') as picklefile:
        TS = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'TD.pickle'), 'r') as picklefile:
        TD = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'AS.pickle'), 'r') as picklefile:
        AS = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'AD.pickle'), 'r') as picklefile:
        AD = pickle.load(picklefile)

    print '------------------TS: ---------------------'
    print TS

    print '------------------AS: ---------------------'
    print AS
    count = 0
    for tmp in AS:
        if tmp[1] == -1:
            count += 1
    print 'AS -1: ', count

    print '------------------TD: ---------------------'
    print TD

    print '------------------AD: ---------------------'
    print AD
    count = 0
    for tmp in AD:
        if tmp[1] == -1:
            count += 1
    print 'AD -1: ', count
    print AD[474]
    
