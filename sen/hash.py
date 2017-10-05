
import numpy as np
import scipy

# For now, this is a Galois Field of prime 4294967291
from fifi import optimal_prime_prime2325 as GF

#
# Helper functions
#
class TwoUnivHash(object):
  def __init__(self, n, t=2):
    self.n = n
    self.t = t
    self.gf = GF()
#    self.modulus = int(2**np.ceil(np.log2(n)))
    self.a, self.b = scipy.random.randint(0, high=4294967291, size=(2))

  def hash(self,x):
    return self.gf.add(self.gf.multiply(x,self.a),self.b) % self.t

class TwoUnivHashSign(TwoUnivHash):
#  def __init__(self, n):
#    self.super(2)

  def hash(self,x):
    thing = ((self.a*x % self.modulus) + self.b % self.modulus) % self.t
    if thing < 0:
      return -1
    else:
      return thing
