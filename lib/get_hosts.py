#!/usr/bin/env python

#
# get_hosts. py : return a list with all hosts in it
#

import os
import re

def get_hosts():
  ret = []

  f = open(os.path.dirname(__file__) + '/../confs/hosts')
  for line in f:
    ret.append(re.sub(r'([^\r\n]+)\r?\n', r'\1', line))
  f.close()

  return ret
