#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rsa
import sys
import os
import os.path
import re
import hashlib
import random
import pickle
import zipfile

__author__ = 'Rightpeter'

enc_pattern = re.compile(r'.*\.enc')
dec_pattern = re.compile(r'.*\.dec')
pickle_pattern = re.compile(r'.*\.pickle')

keywords_set = []


def DSSE_add(username, add_token, enc_file):
    rootdir = os.path.join(os.getcwd(), 'static/db/' + username)
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
        # AD[TD[CalcSha1("#EMPTY#")]] = [TS[CalcSha1("#EMPTY#")], TD[CalcSha1(filename)]]

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


def DSSE_del(username, filename):
    rootdir = os.path.join(os.getcwd(), 'static/db/' + username)

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

    print 'TD[filename_sha1]: ', TD[filename_sha1] ^ Filename_md5_hex
    fHere = TD[filename_sha1] ^ filename_md5_hex
    # del TD[CalcSha1(filename)]

    print '-----------------DSSE_del------------------\n'
    while fHere != -1:
        fNext = AD[fHere][1] ^ filename_md5_hex
        word = sxor(AD[fHere][0], filename_md5)
        word_sha1 = CalcSha1(word)
        word_md5 = int(CalcMD5(word), 16)
        print 'AD[fHere][0]: ', AD[fHere][0]
        print 'fNext: ', fNext
        print 'word: ', word

        print AS[TS[word_sha1] ^ word_md5][0] ^ word_md5
        if CalcSha1(str(AS[TS[word_sha1] ^ word_md5][0] ^ word_md5)) == filename_sha1:
            j = TS[word_sha1] ^ word_md5
            TS[word_sha1] = AS[j][1]
        else:
            i = TS[word_sha1] ^ word_md5
            j = AS[word_sha1][1] ^ word_md5
            while AS[j][0] != filename ^ word_md5 and j != -1:
                i = j
                j = AS[j][1] ^ word_md5

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

    file_path = os.path.join(rootdir, filename + '.enc')
    if os.path.isfile(file_path):
        os.remove(file_path)


def DSSE_search(username, word_sha1, word_md5):
    dbdir = os.path.join(os.getcwd(), 'static/db/' + username)

    zf = zipfile.ZipFile(os.path.join(dbdir, 'zipfile.zip'), 'a')

    with open(os.path.join(dbdir, 'TS.pickle'), 'r') as picklefile:
        TS = pickle.load(picklefile)

    with open(os.path.join(dbdir, 'AS.pickle'), 'r') as picklefile:
        AS = pickle.load(picklefile)

    print TS
    print AS
    file_list = []
    try:
        head = TS[word_sha1] ^ word_md5
    except:
        head = -1

    while head != -1:
        file_list.append(AS[head][0] ^ word_md5)
        head = AS[head][1] ^ word_md5

    print file_list

    tmpdir = os.path.join(os.getcwd(), 'static/tmp/' + username)
    if not os.path.isdir(tmpdir):
        os.makedirs(tmpdir)

    zf = zipfile.ZipFile(os.path.join(tmpdir, word_sha1 + '_search.zip'), 'w')
    for f in file_list:
        filename = str(f) + '.enc'
        zf.write(os.path.join(dbdir, filename), filename)
    zf.close()
    return file_list
