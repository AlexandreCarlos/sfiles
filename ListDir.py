#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)
import os
import ctypes
from os.path import join, getsize
from math import ceil

import dataset

class DiskUsage(object):
    def __init__(self):
        self._sectorsPerCluster = ctypes.c_ulonglong(0)
        self._bytesPerSector = ctypes.c_ulonglong(0)
        self._rootPathName = ctypes.c_wchar_p(u"C:\\")

        self._r = ctypes.windll.kernel32.GetDiskFreeSpaceW(self._rootPathName,
                ctypes.pointer(self._sectorsPerCluster),
                ctypes.pointer(self._bytesPerSector),
                None,
                None,
                )

        print (self._r)

        assert self._r == 1

    def disk_file_size(self, file_size):
        r1 = ceil(float(file_size)/float(self._bytesPerSector.value))  # how many sectors
        r2 = ceil(r1/float(self._sectorsPerCluster.value))

        return long(r2*self._bytesPerSector.value*self._sectorsPerCluster.value)

class Ficheiro(object):
    def __init__(self):
        self._path = ""
        self._filename = ""
        self._size = 0L
        self._disk_size = 0L

        #connect to the database
        self.db = dataset.connect('sqlite:///file_space.db')

        # get a reference to the table 'projetos'
        self.table = self.db['ficheiros']

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def disk_size(self):
        return self._disk_size

    @disk_size.setter
    def disk_size(self, value):
        self._disk_size = value

    def insert(self):
        self.table.insert(dict(path=self._path,
                               filename=self._filename,
                               size=self._size,
                               disk_size=self._disk_size))

    def delete(self, **_filter):
        self.table.delete(**_filter)

    def begin(self):
        self.db.begin()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

du = DiskUsage()
fich = Ficheiro()

# fich.begin()
# fich.delete()
# fich.commit()
fich.begin()

for dirname, dirnames, filenames in os.walk('C:\\Users\\Alexandre\\Documents\\Dropbox\\Python_Books',
topdown=True):
    # print path to all subdirectories first.
    # for subdirname in dirnames:
    #     print join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
        fich.path = dirname
        fich.filename = filename
        fich.size = getsize(join(dirname, filename))
        fich.disk_size = du.disk_file_size(fich.size)
        fich.insert()
        print(join(dirname, filename).encode('utf-8'),
              getsize(join(dirname, filename)), fich.disk_size)

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk()
    # from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')

fich.commit()
