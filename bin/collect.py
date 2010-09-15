#!/usr/bin/env python
import os
import subprocess
import time

import sys
sys.path.append(os.path.dirname(__file__) + '/..')
from lib.rrd import *
from confs.config import *
from lib.log import *

# parse the response from fping
def parse_fping_response(string):
  end_host = string.find(' ')
  start_delay = string.find(':')+2
  host = string[0:end_host]
  
  if string.find('avg') == -1:
    log('fping: no answer, fping output was' + string, 2)
    return (host, 'U')
  
  stats_start = string.find('max')+5
  avg_start = string.find('/', stats_start)+1
  avg_end = string.find('/', avg_start)
  return (host, string[avg_start:avg_end])

# fping a list of hosts, returning a (host, delay) list
def fping(hosts):
  pipe = subprocess.Popen([fping_executable, '-c', str(packets), '-q'] + hosts, 
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) # fping sumarry is on stderr
  delays = pipe.communicate()[1].splitlines()
  return map(parse_fping_response, delays)

# parse the response from ping
def parse_ping_response(string):
  if string.find('avg') == -1:
    log('ping: no answer, ping output was' + string, 2)
    return 'U'

  stats_start = string.find('=')
  avg_start = string.find('/', stats_start)+1
  avg_end = string.find('/', avg_start)
  return string[avg_start:avg_end]

# ping a list of hosts
def ping(hosts):
  for host in hosts:
    pipe = subprocess.Popen([ping_executable, '-c', str(packets), host],
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
    add_value(host, delay)
    log('collecting host' + host + ': delay ' + delay, 1)

if __name__ == "__main__":
  from lib.get_hosts import get_hosts

  log('Collect started', 1)

  tstart = time.time()
  collect(get_hosts())
  tend = time.time() - tstart

  log('Collect finished and ran for ' + str(tend), 1)
