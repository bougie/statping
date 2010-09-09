#!/usr/bin/env python

#
# get_hosts. py : return a list with all hosts in it
#

def get_hosts():
  ret = {}

  f = open('../confs/hosts.cnf')
  for line in f:
    ret.append(sub(r'([^\r\n]+)\r?\n', r'\1', line))
  f.close()

  return ret
