#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os.path import join, getsize

for dirname, dirnames, filenames in os.walk('C:\\Users\\KKU035\\Documents\\Dropbox\\Python_Books', topdown=True):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        print join(dirname, subdirname)

    # print path to all filenames.
    for filename in filenames:
        print join(dirname, filename), getsize(join(dirname, filename)) 

    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk()
    # from recursing into there.
    if '.git' in dirnames:
        # don't go into any .git directories.
        dirnames.remove('.git')
