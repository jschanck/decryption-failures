import os
import sys
from mpmath import mp

mp.prec = 53

ZERO = mp.mpf(0)
APPROX_ZERO = mp.mpf(2**-384)

def log2(x):
    if x == 0:
        return 0
    return mp.log(x, 2)

def binomial(n, i):
    return int(mp.binomial(n, i))

def mod_switch(x, q, rq):
    """ Modulus switching (rounding to a different discretization of the Torus)
    :param x: value to round (integer)
    :param q: input modulus (integer)
    :param rq: output modulus (integer)
    """
    return int(round(1. * rq * x / q) % rq)

def mod_centered(x, q):
    """ reduction mod q, centered (ie represented in -q/2 .. q/2)
    :param x: value to round (integer)
    :param q: input modulus (integer)
    """
    a = x % q
    if a < q/2:
        return a
    return a - q

def jar(f):
    return os.path.join("jar", f.replace("/", "_"))

def p(label, key, val):
    if isinstance(val, int):
        line = "/data/{:s}/{:s}/.initial={:d},".format(label, key, val)
    elif isinstance(val, str):
        line = "/data/{:s}/{:s}/.initial={:s},".format(label, key, val)
    else:
        line = "/data/{:s}/{:s}/.initial={:.1f},".format(label, key, val)
    tex_filename = label.replace("/", "_")
    with open("data/{}".format(tex_filename), "a") as tex:
        print(line, file=tex)

def progress(label, output):
    line = "{}: ".format(label) + output
    log_filename = label.replace("/", "_")
    with open("log/{}".format(log_filename), "a") as log:
        print(line, file=log)
    print(line, file=sys.stderr)
