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

def get_view_graph_path(host):
  return '../' + graph_dir + '/' + host + '.png'

def create_database(host):
  ret = rrdtool.create(get_full_path(host),
                       '--start', 'N',
                       '--step', str(step),
                       'DS:response-time:GAUGE:120:0:U',
                       'RRA:LAST:0.5:1:1440',
                       'RRA:AVERAGE:0.5:5:2000',
                       'RRA:AVERAGE:0.5:60:720')
  if ret:
    raise IOError(rrdtool.error())

def ensure_database_exists(host):
  if not os.path.isfile(get_full_path(host)):
    create_database(host)

def add_value(host, value):
  ensure_database_exists(host)
  ret = rrdtool.update(get_full_path(host),
                       'N:' + value)

  if ret:
    raise IOError(rrdtool.error())

def render(host, start, end):
  if start == '':
    start = default_start

  if end == '':
    end = default_end

  ret = rrdtool.graph(get_full_graph_path(host),
                      '--start', start,
                      '--end', end,
                      '--vertical-label', 'ms',
                      '--title', 'Statping on ' + host,
                      '--width', default_width,
                      '--height', default_height,
                      'DEF:probe1=' + get_full_path(host) + ':response-time:AVERAGE',
                      'AREA:probe1#3333FF:Response time',
                      'VDEF:probe1last=probe1,LAST',
                      'VDEF:probe1min=probe1,MINIMUM',
                      'VDEF:probe1max=probe1,MAXIMUM',
                      'VDEF:probe1avg=probe1,AVERAGE',
                      'VDEF:date=probe1,LAST',
                      'COMMENT:          ',
                      'COMMENT:Current\:',
                      'GPRINT:probe1last:%6.0lf ms\j',
                      'COMMENT:Minimum\:',
                      'GPRINT:probe1min:%6.0lf ms',
                      'COMMENT:Maximum\:',
                      'GPRINT:probe1max:%6.0lf ms',
                      'COMMENT:Average\:',
                      'GPRINT:probe1avg:%6.0lf ms\j',
                      'COMMENT: \j',
                      'GPRINT:date:Last update \: %d/%m/%Y %H\:%M\j:strftime')

  return get_view_graph_path(host)
