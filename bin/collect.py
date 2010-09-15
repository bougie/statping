#!/usr/bin/env python
import os
import subprocess
import time

import sys
sys.path.append(os.path.dirname(__file__) + '/..')
from lib.rrd import *
from confs.config import *

# parse the response from fping
def parse_fping_response(string):
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
                          stderr=subprocess.PIPE) # fping sumarry is on stderr
  delays = pipe.communicate()[1].splitlines()
  return map(parse_fping_response, delays)

# parse the response from ping
def parse_ping_response(string):
  stats_start = string.find('=')
  avg_start = string.find('/', stats_start)+1
  avg_end = string.find('/', avg_start)
  return string[avg_start:avg_end]

# ping a list of hosts
def ping(hosts):
  for host in hosts:
    pipe = subprocess.Popen([ping_executable, '-c', '1', host],
                            stdout=subprocess.PIPE)
    response = pipe.communicate()[0].splitlines()[-1] # last line
    yield (host, parse_ping_response(response))

# collect data
def collect(hosts):
  if ping_method == 'fping':
    responses = fping(hosts)
  else:
    responses = ping(hosts)

  for (host, delay) in responses:
    ensure_database_exists(host)
    add_value(host, delay)

if __name__ == "__main__":
  from lib.get_hosts import get_hosts

  hdl = open(os.path.dirname(__file__) + '/statping.log', 'a')

  tstart = time.time()
  collect(get_hosts())
  tend = time.time() - tstart

  hdl.write(time.strftime("%d/%m/%Y %H:%M:%S : Collect started and ran for " + str(tend) + "\n"))

  hdl.close()
