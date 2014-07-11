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

def DSSE_del(username, filename):
    rootdir = os.path.join(os.getcwd(), 'static/db/'+username)

    with open(os.path.join(rootdir, 'TS.pickle'), 'r') as picklefile:
        TS = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'TD.pickle'), 'r') as picklefile:
        TD = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'AS.pickle'), 'r') as picklefile:
        AS = pickle.load(picklefile)

    with open(os.path.join(rootdir, 'AD.pickle'), 'r') as picklefile:
        AD = pickle.load(picklefile)

    filename_sha1 = CalcSha1(filename)
    filename_md5 = CalcMD5(filename)
    filename_md5_hex = int(filename_md5, 16)

    print 'TD[filename_sha1]: ', TD[filename_sha1]^filename_md5_hex
    fHere = TD[filename_sha1] ^ filename_md5_hex
    #del TD[CalcSha1(filename)]

    print '-----------------DSSE_del------------------\n'
    while fHere != -1:
        fNext = AD[fHere][1] ^ filename_md5_hex
        word = sxor(AD[fHere][0], filename_md5)
        word_sha1 = CalcSha1(word)
        word_md5 = int(CalcMD5(word), 16)
        print 'AD[fHere][0]: ', AD[fHere][0]
        print 'fNext: ', fNext
        print 'word: ', word

        print AS[TS[word_sha1]^word_md5][0]^word_md5
        if CalcSha1(str(AS[TS[word_sha1]^word_md5][0]^word_md5)) == filename_sha1:
            j = TS[word_sha1]^word_md5
            TS[word_sha1] = AS[j][1]
        else:
            i = TS[word_sha1] ^ word_md5
            j = AS[word_sha1][1] ^ word_md5
            while AS[j][0] != filename^word_md5 and j != -1:
                i = j;
                j = AS[j][1]^word_md5

            if j != -1:
                AS[i][1] = AS[j][1]

        AS[j] = ["#EMPTY#", TS[CalcSha1("#EMPTY#")]]
        TS[CalcSha1("#EMPTY#")] = j ^ int(CalcMD5("#EMPTY#"), 16)

        AD[fHere] = ["#EMPTY#", TD[CalcSha1("#EMPTY#")]]
        TD[CalcSha1("#EMPTY#")] = fHere ^ int(CalcMD5("#EMPTY#"), 16)
        fHere = fNext

    with open(os.path.join(rootdir, 'TS.pickle'), 'w+') as outputfile:
        pickle.dump(TS, outputfile)

    with open(os.path.join(rootdir, 'TD.pickle'), 'w+') as outputfile:
        pickle.dump(TD, outputfile)

    with open(os.path.join(rootdir, 'AS.pickle'), 'w+') as outputfile:
        pickle.dump(AS, outputfile)

    with open(os.path.join(rootdir, 'AD.pickle'), 'w+') as outputfile:
        pickle.dump(AD, outputfile)

