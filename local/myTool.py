#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import re

enc_pattern = re.compile(r'.*\.enc$')
dec_pattern = re.compile(r'.*\.dec$')
pickle_pattern = re.compile(r'.*\.dec$')

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

