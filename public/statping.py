#!/usr/bin/env python

import sys
import os
from cgi import FieldStorage, escape
from re import sub
from subprocess import Popen, PIPE

sys.path.append(os.path.dirname(__file__) + "/..")
from lib.get_hosts import *
from lib.gen_graph import *
from confs.config import *

#
# list_hosts : return a html list wich contains hosts list
#
def list_hosts(params):
  html = '<ul>'
  urlhost = params.getvalue('host')

  for host in get_hosts():
    if host == urlhost:
      html += '<li>' + host + '</li>'
    else:
      html += '<li><a href="' + path + '?host=' + host + '">' + host + '</a></li>'

  html += '</ul>'

  return html

#
# gen_menu : generate the side menu
#
def gen_menu(params):
  html = '<div class="menu">';

  html += list_hosts(params)

  html += '</div>';

  return html

#
# gen_renderform : configure and generate render host form
#
def gen_renderform(params):
  html = '<div class="renderform">'

  host = params.getvalue('host') or 'all'
  range = params.getvalue('range') or ''
  begin = params.getvalue('begin') or ''
  end = params.getvalue('end') or ''

  html += '<form method="post" action="' + path + '?host=' + host + '">'
  html += ('<label>Time scale: <select name="range">' +
           '<option value="-1hour">Last hour</option>' +
           '<option value="-1day">Last day</option>' +
           '<option value="-1week">Last week</option>' +
           '<option value="-1month">Last month</option>' +
           '<option value="-1year">Last year</option>' +
           '</select></label>&nbsp;')
  html += ('<label>begin : <input type="text" name="begin"'
           ' value="' + begin + '"/></label>&nbsp;')
  html += ('<label>end : <input type="text" name="end"'
           ' value="' + end + '"/></label>&nbsp;')
  html += '<br /><input type="submit" value="render" />'
  html += '</form>'
  html += '</div>'

  return html

#
# show_host : list graphs associated with an host
#
def show_host(params):
  html = '<div class="host_graphs">'

  host = params.getvalue('host')
  range = params.getvalue('range') or ''
  begin = params.getvalue('begin') or ''
  end = params.getvalue('end') or ''
  
  if host != 'all' and not host in get_hosts():
    return '<p>No such host</p>'

  if range != '' and begin == '':
    begin = range
 
  if host == 'all':
    html += '<h1>Statping for all hosts</h1>'

    for host in get_hosts():
      url = gen_graph(host, begin, end)
      html += '<img src="' + url + ' alt="' + host + '"/><br />'
  else: 
    html += '<h1>Statping for ' + host + '</h1>'

    url = gen_graph(host, begin, end)
    html += '<img src="' + url + ' alt="' + host + '"/>'

  html += '</div>'

  return html

#
#
#
def manage_hosts(params):
  print 'TODO'

### app
def statping(environ, start_response):
  params = FieldStorage(fp=environ['wsgi.input'], environ=environ)
  start_response('200 OK', [('Content-Type', 'text/html'),
                            ('charset', 'utf-8')])
  body = '<html>'
  body += '<head><title>statping</title><link href="style.css" rel="stylesheet" type="text/css" media="screen" /></head>'
  body += '<body>'

  body += gen_menu(params)
  body += gen_renderform(params)

  if 'host' in params:
    body += show_host(params)
  elif admin and 'manage' in params or 'new_hosts' in params:
    body += manage_hosts(params)

  body += '</body>'
  body += '</html>'

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
