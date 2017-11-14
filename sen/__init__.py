# Sublinear_Centrality
# Copyright 2017 Benjamin Priest
# See LICENSE for details.

"""
Sublinear Centrality API library
"""
__version__ = '0.0.0'
__author__ = 'Benjamin W. Priest'
__license__ = 'Apache'

import sen.hash
import sen.sketch
import sen.streaming
import sen.util

#from sen.streaming import CSStreamListener
from tweepy.api import API

# Global, unauthenticated instance of API
api = API()

def debug(enable=True, level=1):
    from six.moves.http_client import HTTPConnection
    HTTPConnection.debuglevel = level
