#!/usr/bin/env python

import os.path
import rrdtool

sys.path.append(os.path.dirname(__file__) + "/..")
from confs.config import *

def create_database(host):
  ret = rrdtool.create(os.path.dirname(__file__) + "/.." + data_dir + '/' + host + '.rrd',
                       '--step', step 
                       'DS:response-time:GAUGE:' + step + ':0:U',
                       'RRA:AVERAGE:0.5:12:1440')
  if ret:
    raise IOError(rrdtool.error())

def ensure_database_exists(host):
  if not os.path.isfile(os.path.dirname(__file__) + "/.." + data_dir + '/' + host + '.rrd'):
    create_database(host)

def add_value(host, value):
  ensure_database_exists(host)
  ret = rrdtool.update(os.path.dirname(__file__) + "/.." + data_dir + '/' + host + '.rrd',
                       'N:' + value)
  if ret:
    raise IOError(rrdtool.error())
