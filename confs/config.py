#!/usr/bin/env python

#
# config.py : configuration variables
#

from time import localtime, strftime

data_dir = ""
graph_dir = ""

admin = True

default_step = 86400
default_begin = strftime("%m/%d/%Y %H:%M", localtime())
