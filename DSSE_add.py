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

def sxor(s1, s2):
    return ''.join(chr(ord(a)^ord(b)) for a,b in zip(s1, s2))

def DSSE_add(username, add_token, enc_file):
    rootdir = os.path.join(os.getcwd(), 'static/db/'+username)
    with open(os.path.join(rootdir, 'TS.pickle'), 'r') as picklefile:
        TS = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'TD.pickle'), 'r') as picklefile:
        TD = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'AS.pickle'), 'r') as picklefile:
        AS = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'AD.pickle'), 'r') as picklefile:
        AD = pickle.load(picklefile)

    filename = add_token[0]
    del add_token[0]
    filename_sha1 = CalcSha1(filename)
    filename_md5 = int(CalcMD5(filename), 16)

    print '-----------------DSSE_add------------------\n'
    TD[filename_sha1] = -1 ^ filename_md5

    for word in add_token:
        word_sha1 = CalcSha1(word)
        word_md5 = int(CalcMD5(word), 16)
        try:
            head = TS[word_sha1]
        except:
            head = -1 ^ word_md5
            
        eTS = TS[CalcSha1("#EMPTY#")] ^ int(CalcMD5("#EMPTY#"), 16)
        eAsNext = AS[eTS][1]
        AS[eTS] = [int(filename) ^ word_md5, head]
        
        eTD = TD[CalcSha1("#EMPTY#")] ^ int(CalcMD5("#EMPTY#"), 16)
        eAdNext = AD[eTD][1]
        AD[eTD] = [sxor(word, CalcMD5(filename)), TD[filename_sha1]]
        #AD[TD[CalcSha1("#EMPTY#")]] = [TS[CalcSha1("#EMPTY#")], TD[CalcSha1(filename)]]

        TS[word_sha1] = eTS ^ word_md5
        TS[CalcSha1("#EMPTY#")] = eAsNext

        TD[filename_sha1] = eTD ^ filename_md5
        TD[CalcSha1("#EMPTY#")] = eAdNext

    with open(os.path.join(rootdir, 'TS.pickle'), 'w+') as outputfile:
        pickle.dump(TS, outputfile)

    with open(os.path.join(rootdir, 'TD.pickle'), 'w+') as outputfile:
        pickle.dump(TD, outputfile)

    with open(os.path.join(rootdir, 'AS.pickle'), 'w+') as outputfile:
        pickle.dump(AS, outputfile)

    with open(os.path.join(rootdir, 'AD.pickle'), 'w+') as outputfile:
        pickle.dump(AD, outputfile)

    with open(os.path.join(rootdir, enc_file['filename']), 'w+') as outputfile:
        outputfile.write(enc_file['body'])
