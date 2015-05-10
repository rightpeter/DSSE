#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re 
import zipfile
import os.path
import os

enc_pattern = re.compile(r'.*\.enc$')
pickle_pattern = re.compile(r'.*\.pickle$')

def zip(user, rootdir):
    zipfile_name = user + '_upload.zip'
    zipdir_path = os.path.join(rootdir, user)
    if not os.path.exists(zipdir_path):
        # print 'No ', zipdir_path
        os.mkdir(zipdir_path)

    zf = zipfile.ZipFile(os.path.join(zipdir_path, zipfile_name), 'w')
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if enc_pattern.match(filename) or pickle_pattern.match(filename):
                file_path = os.path.join(parent, filename)
                zf.write(file_path, filename)
                os.remove(file_path)
    zf.close()


if __name__ == '__main__':
    # print 'argv[0]: ', sys.argv[0]
    # print 'argv[1]: ', sys.argv[1]
    user = sys.argv[1]
    rootdir = os.path.join(os.getcwd(), 'db', user)

    zip(user, rootdir)