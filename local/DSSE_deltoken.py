#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import myTools
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


def deltoken(username, filename):
    rootdir = os.path.join(os.getcwd(), username)
    file_path = os.path.join(rootdir, filename)

    tmpdir = os.path.join(os.getcwd(), 'tmp', username)
    with open(os.path.join(tmpdir, 'del_token.tmp'), 'w+') as outputfile:
        outputfile.write(myTools.CalcSha1(filename) + ' ' + myTools.CalcMD5(filename) + '\n')

if __name__ == '__main__':
    username = sys.argv[1]
    filename = sys.argv[2]

    if not (enc_pattern.match(filename) or dec_pattern.match(filename) or pickle_pattern.match(filename)):
        deltoken(username, filename)
