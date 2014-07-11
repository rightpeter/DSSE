#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re 
import zipfile
import os.path
import os

enc_pattern = re.compile(r'.*\.enc$')
pickle_pattern = re.compile(r'.*\.pickle$')

if __name__ == '__main__':
    print 'argv[0]: ', sys.argv[0]
    print 'argv[1]: ', sys.argv[1]
    rootdir = os.path.join(os.getcwd(), 'db', sys.argv[1])
    user = sys.argv[1]
    print rootdir

    tmpdir = os.path.join(os.getcwd(), 'tmp', sys.argv[1])
    zf = zipfile.ZipFile(os.path.join(tmpdir, 'upload.zip'), 'w')
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if enc_pattern.match(filename) or pickle_pattern.match(filename):
                file_path = os.path.join(parent, filename)
                zf.write(file_path, filename)

    zf.close()
