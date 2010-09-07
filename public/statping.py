#!/usr/bin/env python
from os import system
from cgi import FieldStorage, escape
from re import sub
from time import localtime, strftime

admin = True                    # do we auhorize admin stuff or not ?
generator = '../bin/rendergraph'
img_path = './img/'
conf_path = '../confs/'
default_begin = strftime("%m/%d/%Y %H:%M", localtime())
default_step = '86400'

### "system" functions
def get_hosts():
  f = open(conf_path + 'hosts.cnf')
  for line in f:
    yield sub(r'([^\r\n]+)\r?\n', r'\1', line)
  f.close()

def save_hosts(content):
  f = open(conf_path + 'hosts.cnf', 'w')
  f.write(content)
  f.close()

def gen_graph(host, step, begin):
  # TODO: handle errors
  # TODO: concert begin to a timestamp
  system(reduce(lambda x,y: x + ' ' + y, [generator, host, step, begin]))

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
  step = params.getvalue('step') or default_step
  begin = params.getvalue('begin') or default_begin
  
  html = '<h1>Statping for ' + host + '</h1>'
  
  if not host in get_hosts():
    return '<p>No such host</p>'
  
  # TODO: get default values
  html += '<form method="post" action="/?host=' + host + '">'
  html += ('<label>Time scale: <select name="step">' +
           '<option value="3600">Last hour</option>' +
           '<option value="86400">Last day</option>' +
           '<option value="604800">Last week</option>' +
           '<option value="18144000">Last month</option>' +
           '<option value="6622560000">Last year</option>' +
		   '</select></label><br/>')
  html += ('<label>begin (mm/dd/yyyy hh:ii) : <input type="text" name="begin" value="' + 
           begin + '"/></label><br/>')
  html += '<input type="submit" value="generate" />'
  html += '</form>'
  
  gen_graph(host, step, begin)
  html += '<img src="' + img_path + host + '.png" alt="' + host + '"/>'
  return html

def manage_hosts(params):
  html = '<h1>Manage hosts</h1>'
  if 'new_hosts' in params:
    save_hosts(params.getvalue('new_hosts'))
    return html + '<p>Hosts saved<br/><a href="">back</a></p>'
  
  html += '<form method="post" action="/?manage=t" enctype="multipart/form-data">'
  html += '<textarea name="new_hosts" rows="20" cols="80">\n'
  for host in get_hosts():
    html += host + '\n'
  html += '</textarea><br/>'
  html += '<input type="submit" value="update" />'
  html += '</form>'
  return html

### app
def statping(environ, start_response):
  params = FieldStorage(fp=environ['wsgi.input'], environ=environ)
  start_response('200 OK', [('Content-Type', 'text/html'),
                            ('charset', 'utf-8')])
  body = ''
  if admin:
    body += '<a href="/?manage=t">manage</a> - '
  body += '<a href="/">list</a><br/>'
  if 'host' in params:
    body += show_host(params)
  elif admin and 'manage' in params or 'new_hosts' in params:
    body += manage_hosts(params)
  else:
    body += list_hosts(params)
  return body

### server
def start(port):
  from wsgiref.simple_server import make_server
  srv = make_server('localhost', port, statping)
  srv.serve_forever()

def start_cgi():
  from flup.server.fcgi import WSGIServer
  WSGIServer(statping).run()

if __name__ == "__main__":
  start_cgi()
