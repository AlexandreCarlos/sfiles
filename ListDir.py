#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)
import os
from os.path import join, getsize
import dataset


class Ficheiro(object):
    def __init__(self):
        self._path = ""
        self._filename = ""
        self._size = ""

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

    def insert(self):
        self.table.insert(dict(path=self._path,
                          filename=self._filename,
                          size=self._size))

    def delete(self, **_filter):
        self.table.delete(**_filter)

    def begin(self):
        self.db.begin()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

fich = Ficheiro()

# fich.begin()
# fich.delete()
# fich.commit()
fich.begin()


for dirname, dirnames, filenames in os.walk('C:\\Users\\'
                                            + 'KKU035\\Documents\\'
                                            + 'Dropbox\\Python_Books',
                                            topdown=True):
    # print path to all subdirectories first.
    # for subdirname in dirnames:
    #     print join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
        fich.path = dirname
        fich.filename = filename
        fich.size = getsize(join(dirname, filename))
        fich.insert()
        print (join(dirname, filename).encode('utf-8'),
               getsize(join(dirname, filename)))

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk()
    # from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')

fich.commit()
