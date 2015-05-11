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


def addtoken(username, file_path):
    filename = file_path.split('/')[-1]

    with open(file_path) as inputfile:
        raw_content = inputfile.read()

    spli = raw_content.split()
    keywords = list(set(spli))
    tmpdir = os.path.join(os.getcwd(), 'tmp', username)
    with open(os.path.join(tmpdir, 'add_token.tmp'), 'w+') as outputfile:
        outputfile.write(filename+'\n')
        for word in keywords:
            outputfile.write(word+'\n')

if __name__ == '__main__':
    username = sys.argv[1]
    filename = sys.argv[2]

    if not ( enc_pattern.match(filename)
          or dec_pattern.match(filename)
          or pickle_pattern.match(filename) ):
          addtoken(username, filename)
