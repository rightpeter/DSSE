#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import sys
import os
import myTools

def srchtoken(username, word):
    tmpdir = os.path.join(os.getcwd(), 'tmp', username)

    if not os.path.isdir(tmpdir):
        os.mkdir(tmpdir)

    with open(os.path.join(tmpdir, 'srch_token.tmp'), 'w+') as outputfile:
        outputfile.write(username+' '+myTools.CalcSha1(word)+' '+myTools.CalcMD5(word))

if __name__ == '__main__':
    username = sys.argv[1]
    word = sys.argv[2]

    srchtoken(user, word)
