from functools import partial
from mpmath import mp

from util import log2

from distributions import dist_absolute
from probabilities import expectation, top_quantile

def log_cap(dim, theta):
    return -0.5 * log2(2*mp.pi*dim) - log2(mp.cos(theta)) + (dim-1)*log2(mp.sin(theta))

def queries(x, dim=None, t=None, alpha=None):
    """ returns: 1/C_d(theta) where theta = acos(t/sqrt(alpha*x)) """
    y = mp.sqrt(x*alpha)
    if y < t:
        return 0
    theta = mp.acos(t / y)
    return 2**(log_cap(dim, theta))

def volume_estimate(ps, query_l2_dist, alpha, optimize_e3=False):
    dim = ps.inner_product_dimension()
    threshold = ps.threshold()
    abs_e3_dist = dist_absolute(ps.e3_distribution())
    def crunch(cutoff):
        e3_cutoff = sorted(abs_e3_dist)[cutoff]
        t = threshold - e3_cutoff
        f = partial(queries, dim=dim, t=t, alpha=alpha)
        result = expectation(query_l2_dist, f)
        return result
    cutoff = sorted(abs_e3_dist).index(min(top_quantile(abs_e3_dist,100)))
    result = crunch(cutoff)
    e3_cutoff = sorted(abs_e3_dist)[cutoff]
    if optimize_e3: # Optimize e3_cutoff
        step = 16 #XXX: arbitrary
        while step > 0:
            decreasing = True
            while (len(abs_e3_dist)+cutoff-step > 0) and decreasing:
                candidate = crunch(cutoff-step)
                decreasing = candidate < result
                if decreasing:
                    result = candidate
                    e3_cutoff = sorted(abs_e3_dist)[cutoff-step]
                    cutoff -= step
            step //= 2
    result *= 2 # Account for absolute value bars
    return -log2(result), e3_cutoff
