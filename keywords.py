#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa
import sys
import os
import os.path
import re

enc_pattern = re.compile(r'.*\.enc$')
dec_pattern = re.compile(r'.*\.dec$')

def keywords(parent, filename):
    file_path = os.path.join(parent, filename)
    print '-----------------keywords------------------\n'
    with open(file_path) as inputfile:
        raw_content = inputfile.read()
    

    spli = raw_content.split()
    keywords = list(set(spli))
    print 'keywords: ', keywords 
    #content = content[:245]

    with open(file_path+'.kw', 'w+') as outputfile:
        for word in keywords:
            outputfile.write(word)
            outputfile.write(',')
        outputfile.close()


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
            if not (enc_pattern.match(file_path) or dec_pattern.match(file_path)):
                keywords(parent, filename)
