#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import sys
import os
import re
import random
import pickle
import myTools

enc_pattern = re.compile(r'.*\.enc')
dec_pattern = re.compile(r'.*\.dec')
pickle_pattern = re.compile(r'.*\.pickle')
zip_pattern = re.compile(r'.*\.zip')
int_pattern = re.compile(r'^[1-9]\d*$')

DEBUG = {}
TS = {}
TD = {}
AS = range(1000)
AD = range(1000)
tmp_TS = range(1000)
tmp_TD = range(1000)


def DSSE_index(parent, filename):
    file_path = os.path.join(parent, filename)
    filename_sha1 = myTools.CalcSha1(filename)
    filename_md5 = int(myTools.CalcMD5(filename), 16)
    # print '-----------------index------------------\n'
    with open(file_path) as inputfile:
        raw_content = inputfile.read()

    spli = raw_content.split()
    keywords = list(set(spli))
    # print 'keywords: ', keywords
    TD[filename_sha1] = -1 ^ filename_md5

    for word in keywords:
        word_sha1 = myTools.CalcSha1(word)
        word_md5 = int(myTools.CalcMD5(word), 16)
        try:
            head = TS[word_sha1]
        except:
            head = -1 ^ word_md5
            DEBUG[word] = myTools.CalcSha1(word)

        AS[tmp_TS[0]] = [int(filename) ^ word_md5, head]
        TS[word_sha1] = tmp_TS[0] ^ word_md5

        # print 'word: ', word, 'filename: ', filename, 'sxor: ', sxor(word, CalcMD5(filename)), 'i: ', tmp_TS[0]
        AD[tmp_TD[0]] = [myTools.sxor(word, myTools.CalcMD5(filename)), TD[filename_sha1]]
        # AD[tmp_TD[0]] = [word ^ filename_md5, TD[filename_sha1]]
        TD[filename_sha1] = tmp_TD[0] ^ filename_md5
        del tmp_TS[0]
        del tmp_TD[0]


def index(rootdir):
    random.shuffle(tmp_TS)
    random.shuffle(tmp_TD)

    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            # print "parent is:" + parent
            # print "filename is:" + filename
            file_path = os.path.join(parent, filename)
            # print "the full name of the file is:" + file_path
            if not (enc_pattern.match(filename) or dec_pattern.match(filename)
                    or pickle_pattern.match(filename) or
                    zip_pattern.match(filename)) and int_pattern.match(filename):
                print 'filename: ', filename
                DSSE_index(parent, filename)

    word = "#EMPTY#"
    word_sha1 = myTools.CalcSha1(word)
    word_md5 = int(myTools.CalcMD5(word), 16)
    TS[word_sha1] = -1 ^ word_md5
    while tmp_TS:
        AS[tmp_TS[0]] = ["#EMPTY#", TS[word_sha1]]
        TS[word_sha1] = tmp_TS[0] ^ word_md5
        del tmp_TS[0]

    filename = "#EMPTY#"
    filename_sha1 = myTools.CalcSha1(filename)
    filename_md5 = int(myTools.CalcMD5(filename), 16)
    TD[filename_sha1] = -1 ^ filename_md5
    while tmp_TD:
        AD[tmp_TD[0]] = ["#EMPTY#", TD[filename_sha1]]
        TD[filename_sha1] = tmp_TD[0] ^ filename_md5
        del tmp_TD[0]

    with open(os.path.join(rootdir, 'TS.pickle'), 'w+') as outputfile:
        pickle.dump(TS, outputfile)

    with open(os.path.join(rootdir, 'TD.pickle'), 'w+') as outputfile:
        pickle.dump(TD, outputfile)

    with open(os.path.join(rootdir, 'AS.pickle'), 'w+') as outputfile:
        pickle.dump(AS, outputfile)

    with open(os.path.join(rootdir, 'AD.pickle'), 'w+') as outputfile:
        pickle.dump(AD, outputfile)


if __name__ == '__main__':
    # print 'argv[0]: ', sys.argv[0]
    # print 'argv[1]: ', sys.argv[1]
    rootdir = os.path.join(os.getcwd(), 'db', sys.argv[1])

    index(rootdir)
