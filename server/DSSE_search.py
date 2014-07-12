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
import zipfile
from myTool import *

enc_pattern = re.compile(r'.*\.enc')
dec_pattern = re.compile(r'.*\.dec')


def DSSE_search(username, word_sha1, word_md5):
    dbdir = os.path.join(os.getcwd(), 'static/db/'+username)

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
        file_list.append(AS[head][0]^word_md5)
        head = AS[head][1] ^ word_md5

    print file_list

    tmpdir = os.path.join(os.getcwd(), 'static/tmp/'+username)
    if not os.path.isdir(tmpdir):
        os.makedirs(tmpdir)

    zf = zipfile.ZipFile(os.path.join(tmpdir, word_sha1+'_search.zip'), 'w')
    for f in file_list:
        filename = str(f)+'.enc'
        zf.write(os.path.join(dbdir, filename), filename)
    zf.close()
    return file_list

