#!/usr/bin/env python

#
# config.py : configuration variables
#

from time import localtime, strftime

path = '' #base url

data_dir = "" #relativ path from statping home
graph_dir = "" #relativ path from statping home
step = 60

admin = True

default_range = "-1day" #Format rrdtool

ping_method = 'ping' # ping of fping
fping_executable = 'fping' # full path to fping
ping_executable = 'ping' # full path to ping

