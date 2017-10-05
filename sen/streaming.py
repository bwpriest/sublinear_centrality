
import array
import logging
import hashlib
import os
import re
import scipy

import sen.hash

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



class CountSketch(object):
    """
    Pure pythonic implementation of CountSketch. Creates a linear transform
    equivalent to an (m*d) x n matrix with d nonzero entries per column. 
    Includes a method for querying 

    :param m: Dimension of hash tables
    :param d: Number of hash tables
    :param n: Dimension of frequency list, if known

    *M. Charikar*, *K. Chen* and *M. Farach-Colton*, **Finding Frequent 
    Items in Data Streams**, Automata, Langauges, and Programming 2002
    """

    def __init__(self, m, d, n = 0):
        """ 
        Initialize CountSketch data object, including coinflips and hash
        functions. 
        """
        if not m or not d:
            raise ValueError("Table size (m) and amount of hash functions (d)"
                             " must be non-zero")
        self.m = m
        self.d = d
        self.n = n
        self.tables = []
        for _ in xrange(d):
            table = array.array("l", (0 for _ in xrange(m)))
            self.tables.append(table)

    def _hash(self, x):
        md5 = hashlib.md5(str(hash(x)))
        for i in xrange(self.d):
            md5.update(str(i))
            yield int(md5.hexdigest(), 16) % self.m

    def add(self, x, value=1):
        """
        Update frequency index `x` with `value`.
        By default `value=1` so:
            sketch.add(x)
        Effectively updates `x` as occurring once.
        """
        self.n += value
        for table, i in zip(self.tables, self._hash(x)):
            table[i] += value

    def query(self, x):
        """
        Return an estimation of the amount of times `x` has ocurred.
        The returned value always overestimates the real value.
        """
        return min(table[i] for table, i in zip(self.tables, self._hash(x)))

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

