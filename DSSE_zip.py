#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import re 
import zipfile
import os.path
import os

enc_pattern = re.compile(r'.*\.enc$')
pickle_pattern = re.compile(r'.*\.pickle$')

class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self,filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)

    def addfile(self, path, arcname=None):
        path = path.replace('//', '/')
        if not arcname:
            if path.startswith(self.basedir):
                arcname = path[len(self.basedir):]
            else:
                arcname = ''
        self.zfile.write(path, arcname)

    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)

    def close(self):
        self.zfile.close()

    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)

    def extract(self, filename, path):
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dir = os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            file(f, 'wb').write(self.zfile.read(filename))

def create(zfile, files):
    z = ZFile(zfile, 'w')
    z.addfiles(files)
    z.close()

def extract(zfile, path):
    z = ZFile(zfile)
    z.extract_to(path)
    z.clsoe()

if __name__ == '__main__':
    print 'argv[0]: ', sys.argv[0]
    print 'argv[1]: ', sys.argv[1]
    rootdir = os.path.join(os.getcwd(), sys.argv[1])
    user = sys.argv[1]
    print rootdir

    zf = zipfile.ZipFile(os.path.join(rootdir,'upload.zip'), 'w')
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if enc_pattern.match(filename) or pickle_pattern.match(filename):
                file_path = os.path.join(parent, filename)
                zf.write(file_path, filename)

    zf.close()
