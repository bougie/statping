#!/usr/bin/env python

import os.path
import rrdtool

import sys
sys.path.append(os.path.dirname(__file__) + "/..")
from confs.config import *

def get_full_path(host):
  return (os.path.dirname(__file__) + '/../' + data_dir + '/' + host + '.rrd')

def get_full_graph_path(host):
  return (os.path.dirname(__file__) + '/../' + graph_dir + '/' + host + '.png')

def create_database(host):
  ret = rrdtool.create(get_full_path(host),
                       '--step', str(step),
                       'DS:response-time:GAUGE:' + str(step) + ':0:U',
                       'RRA:LAST:0.5:1:60',
                       'RRA:LAST:0.5:1:1440',
                       'RRA:AVERAGE:0.5:5:2000',
                       'RRA:AVERAGE:0.5:60:720')
  if ret:
    raise IOError(rrdtool.error())

def ensure_database_exists(host):
  if not os.path.isfile(get_full_path(host))
    create_database(host)

def add_value(host, value):
  ensure_database_exists(host)
  ret = rrdtool.update(get_full_path(host)
                       'N:' + value)
  if ret:
    raise IOError(rrdtool.error())

def render(host, start, end):
  graph_link = get_full_graph_path(host)

  ret = rrdtool.graph(get_full_graph_path(host),
                      '-a', 'PNG'
                      '--start', str(start),
                      '--end', str(end),
                      '--vertical-label=ms',
                      'DEF:probe1=' + get_full_path(host) + ':response-time:AVERAGE',
                      'LINE1:probe1#000000: Response time')

  if ret:
    raise IOError(rrdtool.error())

  return graph_link
