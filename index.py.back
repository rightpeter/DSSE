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
DEBUG = {}
TS = {}
TSt = {}
TD = {}
TDt = {}
AS = range(1000)
AD = range(1000)

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

def index(parent, filename):
    file_path = os.path.join(parent, filename)
    tmp_TS = range(1000)
    random.shuffle(tmp_TS) 
    tmp_TD = range(1000)
    random.shuffle(tmp_TD)
    print '-----------------index------------------\n'
    with open(file_path) as inputfile:
        raw_content = inputfile.read()
    
    spli = raw_content.split()
    keywords = list(set(spli))
    print 'keywords: ', keywords 
    #content = content[:245]
    TD[CalcSha1(filename)] = tmp_TD[0]
    i = tmp_TD[0]
    TDt[CalcSha1(filename)] = tmp_TD[0]

    for word in keywords:
        try:
            head = TS[CalcSha1(word)]
        except:
            head = -1
            DEBUG[word] = CalcSha1(word)
            print '-------word---------\n'
            print word
            print '-------wwww---------\n'
            
       
        AS[tmp_TS[0]] = [filename, head]
        TS[CalcSha1(word)] = tmp_TS[0]
        del tmp_TS[0]

        #if word not in keywords_set:
        #    keywords_set.append(word)
        #    TS[CalcSha1(word)] = tmp_TS[0]
        #    DEBUG[word] = CalcSha1(word)
        #    print '-------word---------\n'
        #    print word
        #    print '-------wwww---------\n'
        #    AS[tmp_TS[0]] = [filename, -1]
        #    #TSt[CalcSha1(word)] = tmp_TS[0]
        #    del tmp_TS[0]
        #else:
        #    AS[tmp_TS[0]] = [filename, -1]
        #    AS[TSt[CalcSha1(word)]][1] = tmp_TS[0]
        #    TSt[CalcSha1(word)] = tmp_TS[0]
        #    del tmp_TS[0]

        #TS[CalcSha1(word)] = tmp_TS[0]
        #AS[tmp_TS[0]] = [filename, -1] 
        #TD[CalcSha1(filename)] = tmp_TD[0]
        AD[tmp_TD[0]] = [tmp_TS[0], TDt[CalcSha1(filename)]]
        TD[CalcSha1(filename)] = tmp_TS[0]
        del tmp_TD[0]


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
            if not ( enc_pattern.match(filename) or dec_pattern.match(filename)
                    or pickle_pattern.match(filename)):
                index(parent, filename)

    with open(os.path.join(parent, 'TS.pickle'), 'w+') as outputfile:
        pickle.dump(TS, outputfile)

    with open(os.path.join(parent, 'TD.pickle'), 'w+') as outputfile:
        pickle.dump(TD, outputfile)

    with open(os.path.join(parent, 'AS.pickle'), 'w+') as outputfile:
        pickle.dump(AS, outputfile)

    with open(os.path.join(parent, 'AD.pickle'), 'w+') as outputfile:
        pickle.dump(AD, outputfile)

    with open(os.path.join(parent, 'KW.pickle'), 'w+') as outputfile:
        pickle.dump(keywords_set, outputfile)

    print TS
    print TD
    print AS
    print AD
    print DEBUG
