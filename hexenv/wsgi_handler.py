#!/usr/bin/env python2.7
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hexenv.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
