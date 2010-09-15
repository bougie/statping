import os.path
import sys
import time
sys.path.append(os.path.dirname(__file__) + "/..")
from confs.config import *

def log(string, level):
  if level <= log_level:
    f = open(os.path.dirname(__file__) + '/../' + log_file, 'a')
    actual_time = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
    f.write(actual_time + ': ' + string + '\n')
    f.close()
    
