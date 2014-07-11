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

def sxor(s1, s2):
    return ''.join(chr(ord(a)^ord(b)) for a,b in zip(s1, s2))

def DSSE_index(parent, filename):
    file_path = os.path.join(parent, filename)
    filename_sha1 = CalcSha1(filename)
    filename_md5 = int(CalcMD5(filename), 16)
    print '-----------------index------------------\n'
    with open(file_path) as inputfile:
        raw_content = inputfile.read()
    
    spli = raw_content.split()
    keywords = list(set(spli))
    print 'keywords: ', keywords 
    TD[filename_sha1] = -1 ^ filename_md5

    for word in keywords:
        word_sha1 = CalcSha1(word)
        word_md5 = int(CalcMD5(word), 16)
        if word not in keywords_set:
            keywords_set.append(word)
        try:
            head = TS[word_sha1]
        except:
            head = -1 ^ word_md5
            DEBUG[word] = CalcSha1(word)
       
        AS[tmp_TS[0]] = [int(filename) ^ word_md5, head]
        TS[word_sha1] = tmp_TS[0] ^ word_md5

        print 'word: ', word, 'filename: ', filename, 'sxor: ', sxor(word, CalcMD5(filename)), 'i: ', tmp_TS[0]
        AD[tmp_TD[0]] = [sxor(word, CalcMD5(filename)), TD[filename_sha1]]
        #AD[tmp_TD[0]] = [word ^ filename_md5, TD[filename_sha1]]
        TD[filename_sha1] = tmp_TD[0] ^ filename_md5
        del tmp_TS[0]
        del tmp_TD[0]

if __name__ == '__main__':
    print 'argv[0]: ', sys.argv[0]
    print 'argv[1]: ', sys.argv[1]
    rootdir = os.path.join(os.getcwd(), sys.argv[1])
    print rootdir

    tmp_TS = range(1000)
    random.shuffle(tmp_TS) 
    tmp_TD = range(1000)
    random.shuffle(tmp_TD)
    
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            print "parent is:" + parent
            print "filename is:" + filename
            file_path = os.path.join(parent, filename)
            print "the full name of the file is:" + file_path
            if not ( enc_pattern.match(filename) or dec_pattern.match(filename)
                    or pickle_pattern.match(filename)):
                DSSE_index(parent, filename)

    word = "#EMPTY#"
    word_sha1 = CalcSha1(word)
    word_md5 = int(CalcMD5(word), 16)
    TS[word_sha1] = -1 ^ word_md5
    while tmp_TS:
        AS[tmp_TS[0]] = ["#EMPTY#", TS[word_sha1]]
        TS[word_sha1] = tmp_TS[0] ^ word_md5
        del tmp_TS[0]

    filename = "#EMPTY#"
    filename_sha1 = CalcSha1(filename)
    filename_md5 = int(CalcMD5(filename), 16)
    TD[filename_sha1] = -1 ^ filename_md5
    while tmp_TD:
        AD[tmp_TD[0]] = ["#EMPTY#", TD[filename_sha1]]
        TD[filename_sha1] = tmp_TD[0] ^ filename_md5
        del tmp_TD[0]

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
    print len(keywords_set)
    print AD[474]
