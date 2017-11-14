import numpy as np

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
