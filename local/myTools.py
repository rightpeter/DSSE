#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import re
import pickle
import datetime
import os

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


def sxor(s1, s2):
    return ''.join(chr(ord(a)^ord(b)) for a,b in zip(s1, s2))


def GetDataDict():
    try:
        with open('mydata.pickle', 'rb') as input:
            data_dict = pickle.load(input)
    except:
        data_dict = {}
        print 'Unable to open mydata.pickle!'
    return data_dict


def GetUserName():
    data_dict = GetDataDict()

    return data_dict.get('username', 'Unset')


def SetUserName(username):
    data_dict = GetDataDict()

    data_dict['username'] = username

    with open('mydata.pickle', 'wb') as output:
        pickle.dump(data_dict, output)


def GetLastGenTime():
    data_dict = GetDataDict()
    return data_dict.get('last_gen_time', 'never gen')


def SetLastGenTime(last_gen_time):
    data_dict = GetDataDict()

    data_dict['last_gen_time'] = last_gen_time

    with open('mydata.pickle', 'wb') as output:
        pickle.dump(data_dict, output)


def GetNowString():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')
