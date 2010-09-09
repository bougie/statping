#!/usr/bin/env python
import sys
import os
from os import system
from cgi import FieldStorage, escape
from re import sub
from subprocess import Popen, PIPE

sys.path.append(os.path.dirname(__file__) + "/..")
from lib.get_hosts import *
from confs.config import *

path = ''

### pages
def list_hosts(params):
  html = '<h1>Hosts</h1><ul>'
  for host in get_hosts():
    html += '<li><a href="' + path + '?host=' + host + '">' + host + '</a></li>'
  html += '</ul>'
  return html

def show_host(params):
  host = params.getvalue('host')
  step = params.getvalue('step') or default_step
  begin = params.getvalue('begin') or default_begin
  
  html = '<h1>Statping for ' + host + '</h1>'
  
  if not host in get_hosts():
    return '<p>No such host</p>'
  
  html += '<form method="post" action="' + path + '?host=' + host + '">'
  html += ('<label>Time scale: <select name="step">' +
           '<option value="3600">Last hour</option>' +
           '<option value="86400">Last day</option>' +
           '<option value="604800">Last week</option>' +
           '<option value="18144000">Last month</option>' +
           '<option value="6622560000">Last year</option>' +
		   '</select></label><br/>')
  html += ('<label>begin (mm/dd/yyyy hh:ii) : <input type="text" name="begin"'
           'value="' + begin + '"/></label><br/>')
  html += '<input type="submit" value="generate" />'
  html += '</form>'
  
  errors = gen_graph(host, step, begin)
  if errors != '':
    html += '<p>Errors: <br/><pre>' + sub('\n', '<br/>', errors) + '</pre></p>'
  html += '<img src="' + img_path + host + '.png" alt="' + host + '"/>'
  return html

### app
def statping(environ, start_response):
  params = FieldStorage(fp=environ['wsgi.input'], environ=environ)
  start_response('200 OK', [('Content-Type', 'text/html'),
                            ('charset', 'utf-8')])
  body = ''
  if admin:
    body += '<a href="' + path + '?manage=t">manage</a> - '
  body += '<a href="' + path + '">list</a><br/>'
  if 'host' in params:
    body += show_host(params)
  elif admin and 'manage' in params or 'new_hosts' in params:
    body += manage_hosts(params)
  else:
    body += list_hosts(params)
  return body

### server
def start_server(port):
  from wsgiref.simple_server import make_server
  srv = make_server('localhost', port, statping)
  srv.serve_forever()

def start_cgi():
  from flup.server.fcgi import WSGIServer
  WSGIServer(statping).run()

if __name__ == "__main__":
  argc = len(sys.argv)

  if argc == 0 or argc == 1:
    start_cgi()
  elif argc == 3 and sys.argv[1] == '-d':
    start_server(sys.argv[2])
  else:
    print 'Error'
