#!/usr/local/bin/python
import os, sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(cur_dir)
sys.path.append(cur_dir + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
 
import django.core.handlers.wsgi
 
application = django.core.handlers.wsgi.WSGIHandler()
