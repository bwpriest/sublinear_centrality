
import array
import logging
import numpy as np
import os
import re
import scipy

from tweepy.streaming import StreamListener
from tweepy.api import API

class CSStreamListener(StreamListener):
    """
    Implementation of tweepy StreamListener class. Intended to scrape live twitter 
    statuses and perform operations thereon. 
    """
    def __init__(self, api=None):
        self.api = api or API()
        self.pattern = re.compile(r'@([^\W@]+)')
        
    def on_status(self, status):
        print(status.text)
#        ppl = self.pattern.findall(status.text)
        

#    def on_direct_message(self, status):
#        print(status.text)
        
    def on_error(self, status_code):
        if status_code == 420:
            return False

class SimpleGraphGenerator(object):
    """
    Collects all files of a specified extension recursively in a specified 
    directory and assembles them into a single graph generator, which can 
    then be generated line by line, mimicking an edge stream. 

    Assumes that the files in question have the format:

        edge_out \t edge_in (\t weight)
    """
    def __init__(self, top_dir, **kwargs):
        self.pattern = re.compile(r'[0-9]+')
        self.graph_generator = iter_documents(top_dir, **kwargs)

    def __iter__(self):
        for line in self.graph_generator:
            yield split_iter(line, self.pattern)


def iter_documents(top_dir, file_ext=".gph"):
    """
    Generator: iterate over all relevant documents, yielding one
    document (=list of utf8 tokens) at a time.
    """
    # find all .txt documents, no matter how deep under top_directory
    for root, dirs, files in os.walk(top_dir):
        for fname in filter(lambda fname: fname.endswith(file_ext), files):
            # read each document as one big string
            document = open(os.path.join(root, fname))
            # break document into utf8 tokens
            for line in document:
                yield line
#            yield gensim.utils.tokenize(document, lower=True, errors='ignore')

def split_iter(string, pattern):
    return (x.group(0) for x in pattern.finditer(string))
