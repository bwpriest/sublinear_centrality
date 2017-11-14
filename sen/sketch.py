import logging
import numpy as np

from sen.hash import TwoUnivHash
from sen.util import _is_power2
from sen.util import _next_power2

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
            # Add 1 for 1-indexing
            yield self.h[i].hash(x+1)

    def _orient(self, x):
        for i in xrange(self.d):
            # Add 1 for 1-indexing
            if self.g[i].hash(x+1):
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
