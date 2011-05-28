#!/usr/bin/env python

#
# get_hosts. py : return a list with all hosts in it
#

import os

def get_hosts():
  f = open(os.path.dirname(__file__) + '/../confs/hosts')
  ret = f.read().splitlines()
  f.close()

  return ret
