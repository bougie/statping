#!/usr/bin/env python
from os import system
from cgi import FieldStorage, escape

generator = './rendergraph'
img_path = ''

### "system" functions
def get_hosts():
  f = open('hosts.cnf')
  for line in f:
    yield line[:-1]
  f.close()

def gen_graph(host):
  system(generator + ' ' + host)

### pages
def list_hosts(params):
  html = '<h1>Hosts</h1><ul>'
  for host in get_hosts():
    html += '<li><a href="?host=' + host + '">' + host + '</a></li>'
  html += '</ul>'
  return html

def show_host(params):
  # TODO: change the step etc.
  host = params.getvalue('host')
  html = '<h1>Statping for ' + host + '</h1>'

  if not host in get_hosts():
    return '<p>No such host</p>'
  
  gen_graph(host)
  html += '<img src="' + img_path + host + '.png" alt="' + host + '"/>'
  return html


### app
def statping(environ, start_response):
  params = FieldStorage(fp=environ['wsgi.input'], environ=environ)
  start_response('200 OK', [('Content-Type', 'text/html'),
                            ('charset', 'utf-8')])
  body = ''
  if 'host' in params:
    body += show_host(params)
  else:
    body += list_hosts(params)
  return body

### server
def start(port):
  from wsgiref.simple_server import make_server
  srv = make_server('localhost', port, statping)
  srv.serve_forever()
