#!/usr/bin/env python

#
# gen_graph.py : generate a graph an return an absolute path to it
#

import rrd

def gen_graph(host, start = '', end = ''):
  return rrd.render(host, start, end)

if __name__ == "__main__":
  from lib.get_hosts import get_hosts

  for host in get_hosts():
    gen_graph(host, '', '');
