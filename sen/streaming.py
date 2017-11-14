
import array
import logging
import numpy as np
import os
import re
import scipy

from tweepy.streaming import StreamListener
from tweepy.api import API

from sen.hash import TwoUnivHash

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



class CountSketch(object):
    """
    Pythonic implementation of CountSketch. Creates a linear transform equivalent 
    to an (d*m) x n matrix with d nonzero entries per column. Includes a method for 
    querying the accumulated estimator of an index's value. 

    :param n: Dimension of frequency vector
    :param m: Dimension of hash tables
    :param d: Number of hash tables

    *M. Charikar*, *K. Chen* and *M. Farach-Colton*, **Finding Frequent 
    Items in Data Streams**, Automata, Langauges, and Programming 2002
    """

    def __init__(self, n, m, d=1):
        """ 
        Initialize CountSketch data object, including coinflips and hash
        functions. 
        """
        if not n or not m or not d:
            raise ValueError("Vector dimension (n), projection dimension (m) "
                             "and number of parallel tables (d) must be non-zero")
        if not _is_power2(m):
            raise ValueError("Projection dimension (m) must be a power of two.")
        
        if _is_power2(n):
            self.n = long(np.log2(n))
        else:
            self.n = long(np.log2(_next_power2(n)))
        self.m = long(np.log2(m))
        self.d = long(d)
        self.sketches = np.zeros((d,m), dtype=long)
        
        self.h = np.array([TwoUnivHash(self.n, self.m) 
                           for i in xrange(d)])
        self.g = np.array([TwoUnivHash(self.n, 2l) 
                           for i in xrange(d)])

    def _hash(self, x):
        for i in xrange(self.d):
            yield self.h[i].hash(x)

    def _orient(self, x):
        for i in xrange(self.d):
            if self.g[i].hash(x):
                yield 1l
            else:
                yield -1l

    def add(self, x, value=1):
        """
        Update frequency index `x` with `value`.
        By default `value=1` so:
            sketch.add(x)
        Effectively updates `x` as occurring once.
        """
        for s, i, o in zip(self.sketches, self._hash(x), self._orient(x)):
            s[i] += o*value

    def query(self, x):
        """
        Return an estimation of the frequency index x.
        The returned value comes from an unbiased estimator.
        """
        return np.median([o*s[i] for s, i, o 
                   in zip(self.sketches, self._hash(x), self._orient(x))])

    def __getitem__(self, x):
        """
        A convenience method to call `query`.
        """
        return self.query(x)

    def __len__(self):
        """
        The amount of things counted. Takes into account that the `value`
        argument of `add` might be different from 1.
        """
        return self.n

def _is_power2(m):
    return m and not m & m-1

def _next_power2(m):
    m |= m >> 1
    m |= m >> 2
    m |= m >> 4
    m |= m >> 8
    m |= m >> 16
    m |= m >> 32
    return m + 1
