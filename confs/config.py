#!/usr/bin/env python

#
# config.py : configuration variables
#

from time import localtime, strftime

path = '' #base url

data_dir = "data" #relativ path from statping home
graph_dir = "public/graphs" #relativ path from statping home
step = 60

admin = True
log_level = 1
log_file = 'statping.log'

# Graph rendering
default_start = "-1day" #Format rrdtool
default_end = "N" #Format rrdtool
default_width = '640'
default_height = '200'

packets = 3 # number of packets to send
ping_method = 'fping' # ping of fping
fping_executable = 'fping' # full path to fping
ping_executable = 'ping' # full path to ping

