import ctypes

from numpy.random import randint

lib = ctypes.cdll.LoadLibrary('/Users/priest/repos/sublinear_centrality/build/libhash.so')

class TwoUnivHash(object):
#    def __init__(self, mul, add, u_dom, u_ran):
    def __init__(self, u_dom, u_ran):
        """
        Randomly sample a multiply-add-shift 2-universal hash 
        function h: [2^u_dom] -> [2^u_ran]
        """
        lib.TwoUnivHash_new.argtypes = [ctypes.c_uint]
        lib.TwoUnivHash_new.restype = ctypes.c_void_p
        lib.TwoUnivHash_members.argtypes = [ctypes.c_void_p]
        lib.TwoUnivHash_members.restype = ctypes.c_void_p
        lib.TwoUnivHash_hash.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        lib.TwoUnivHash_hash.restype = ctypes.c_uint

        # Randomly sample an odd member of [2^u_dom]
        mul = 2*randint(1, high=2**(u_dom-1)+1)-1
        # Randonly sample a member of [2^u_ran]
        add = randint(2**u_ran)
        self.obj = lib.TwoUnivHash_new(mul, add, u_dom, u_ran)

    def members(self):
        """
        Print the members of the underlying C++ class.
        """
        return lib.TwoUnivHash_members(self.obj)
    
    def hash(self, x):
        """
        Return h(x) = (mul*x + add) mod 2^u_dom >> (u_dom - u_ran)
        """
        return lib.TwoUnivHash_hash(self.obj, x)