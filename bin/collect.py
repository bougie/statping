#!/usr/bin/env python
import os
import subprocess

import sys
sys.path.append(os.path.dirname(__file__) + '/..')
from lib.rrd import *
from confs.config import *


# parse the response from fping
def parse_response(string):
  end_host = string.find(' ')
  start_delay = string.find(':')+2

  host = string[0:end_host]
  delay = string[start_delay:]
  if delay == '-':
    return (host, 'U')
  else:
    return (host, delay)

# fping a list of hosts, returning a (host, delay) list
def fping(hosts):
  pipe = subprocess.Popen([fping_executable, '-C', '1', '-q'] + hosts, 
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
  delays = pipe.communicate()[1].splitlines()
  return map(parse_response, delays)

# collect data
def collect(hosts):
  for (host, delay) in fping(hosts):
    ensure_database_exists(host)
    add_value(host, delay)

if __name__ == "__main__":
  from lib.get_hosts import get_hosts
  collect(get_hosts())
