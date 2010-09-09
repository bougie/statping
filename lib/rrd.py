#!/usr/bin/env python

import os.path
import rrdtool

databases_path = '/tmp/'

def create_database(host):
  ret = rrdtool.create(databases_path + host + '.rrd',
                       '--step', '60'
                       'DS:response-time:GAUGE:60:0:999',
                       'RRA:AVERAGE:0.5:3:100')
  if ret:
    raise IOError(rrdtool.error())

def ensure_database_exists(host):
  if not os.path.isfile(databases_path + host + '.rrd'):
    create_database(host)

def add_value(host, value):
  ensure_database_exists(host)
  ret = rrdtool.update(databases_path + host + '.rrd',
                       'N:' + value)
  if ret:
    raise IOError(rrdtool.error())
