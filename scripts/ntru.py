from util import log2
from probabilities import top_quantile,expectation
from distributions import dist_convolution,\
                          dist_scale,\
                          dist_iter_convolution

class NTRUHPS:
    def __init__(self, n, q, improper=False):
        self.n = n
        self.q = q
        self.wt = q//8-2
        self.improper = improper

        self.cache_dist_1 = None
        self.cache_dist_2 = None
        self.cache_dist_3 = None

    def rounds_pk(self):
        return False

    def rounds_c1(self):
        return False

    def rounds_c2(self):
        return False

    def fixed_wt(self):
        return False

    def inner_product_dimension(self):
        return 2 * (self.n-1)

    def threshold(self):
        if self.improper: # a = 3rg + 3Fm + m
            t = self.q // 2 - 2
        else:          # a = 3rg + fm
            t = self.q // 2 - 1
        return t

    def secret_l2_distribution(self):
        if self.cache_dist_1 is None:
            t = {0:1/3, 1:2/3}
            Df = dist_iter_convolution(t, self.n-1)
            if self.improper:
                Df = dist_scale(Df, 9)
            Dg = {9*self.wt: 1}
            self.cache_dist_1 = (Df, Dg)
        return self.cache_dist_1

    def query_l2_distribution(self):
        # r - ternary
        # m - fixed wt q/8 - 2
        if self.cache_dist_2 is None:
            Dr = {self.n-1: 1}
            Dm = {self.wt:  1}
            self.cache_dist_2 = (Dm, Dr)
        return self.cache_dist_2

    def e3_distribution(self):
        return {0:1}

    def one_shot_distribution(self):
        if self.cache_dist_3 is None:
            t = {-1:1/3, 0:1/3, 1:1/3}
            Dfm = dist_iter_convolution(t, self.wt)
            if self.improper:
                Dfm = dist_scale(Dfm, 3)
            t = {-3:1/2, 3:1/2}
            Dgr = dist_iter_convolution(t, self.wt)
            self.cache_dist_3 = dist_convolution(Dfm, Dgr)
        return self.cache_dist_3

    def one_shot_s_quantile(self, lgu):
        t = {0: 1/3, 1:2/3}
        D = dist_iter_convolution(t, self.n-1)
        pnz = expectation(top_quantile(D, 2**(lgu//2)))/(self.n-1)
        t = {-1:pnz/2, 0:1-pnz, 1:pnz/2}
        Dfm = dist_iter_convolution(t, self.wt)
        if self.improper:
            Dfm = dist_scale(Dfm, 3)
        t = {-3:1/2, 3:1/2}
        Dgr = dist_iter_convolution(t, self.wt)
        return dist_convolution(Dfm, Dgr)


class NTRUHRSS:
    def __init__(self, n, q=None, improper=False):
        self.n = n
        if q is None:
            self.q = int(2**round(0.5 + 3.5 + log2(n)))
        else:
            self.q = q
        self.improper = improper

        self.cache_dist_1 = None
        self.cache_dist_2 = None
        self.cache_dist_3 = None

    def rounds_pk(self):
        return False

    def rounds_c1(self):
        return False

    def rounds_c2(self):
        return False

    def fixed_wt(self):
        return False

    def inner_product_dimension(self):
        return 2 * (self.n-1)

    def threshold(self):
        if self.improper:
            t = (self.q // 2 - 1)/(2**0.5) - 1
        else:
            t = (self.q // 2 - 1)/(2**0.5)
        return t

    def secret_l2_distribution(self):
        if self.cache_dist_1 is None:
            t = {0:1/3, 1:2/3}
            Df = dist_iter_convolution(t, self.n-1)
            Dg = dist_scale(Df, 3**2)
            if self.improper:
                Df = dist_scale(Df, 3**2)
            self.cache_dist_1 = (Df, Dg)
        return self.cache_dist_1

    def query_l2_distribution(self):
        # r - ternary
        # m - ternary
        if self.cache_dist_2 is None:
            Dr = {self.n-1: 1}
            Dm = {self.n-1: 1}
            self.cache_dist_2 = (Dm, Dr)
        return self.cache_dist_2

    def e3_distribution(self):
        return {0:1}

    def one_shot_distribution(self):
        if self.cache_dist_3 is None:
            t = {-1:1/3, 0:1/3, 1:1/3}
            Dfm = dist_iter_convolution(t, self.n-1)
            Dgr = dist_scale(Dfm, 3)
            if self.improper:
                Dfm = dist_scale(Dfm, 3)
            self.cache_dist_3 = dist_convolution(Dfm, Dgr)
        return self.cache_dist_3

    def one_shot_s_quantile(self, lgu):
        t = {0: 1/3, 1:2/3}
        D = dist_iter_convolution(t, self.n-1)
        pnz = expectation(top_quantile(D, 2**(lgu/2)))/(self.n-1)
        t = {-1:pnz/2, 0:1-pnz, 1:pnz/2}
        Dfm = dist_iter_convolution(t, self.n-1)
        Dgr = dist_scale(Dfm, 3)
        if self.improper:
            Dfm = dist_scale(Dfm, 3)
        return dist_convolution(Dfm, Dgr)

if __name__ == "__main__":
    import pickle

    from mpmath import mp
    from util import jar, p, progress
    from probabilities import expectation_of_convolution, \
                              tail_probability
    from volume_estimate import volume_estimate
    from parameters import *

    def setup(label, ps):
        progress(label, "starting setup")
        try:
            with open(jar(label), "rb") as brine:
                ps = pickle.load(brine)
        except IOError:
            progress(label, "generating distributions")

        secret_l2_dist = ps.secret_l2_distribution()
        query_l2_dist = ps.query_l2_distribution()
        one_shot_dist = ps.one_shot_distribution()

        f = tail_probability(one_shot_dist, ps.threshold())
        p(label, "oneshot", float(-log2(f)))

        with open(jar(label), "wb") as brine:
            pickle.dump(ps, brine)

    def do(label, lgsq, lgeq):
        with open(jar(label), "rb") as brine:
            ps = pickle.load(brine)

        progress(label, "starting s/{}/e/{}".format(lgsq, lgeq))
        f = tail_probability(ps.one_shot_s_quantile(lgsq), ps.threshold())
        p(label, "s/{}/e/{}/cost".format(lgsq, lgeq), float(-log2(f)))
        progress(label, "done s/{}/e/{}".format(lgsq, lgeq))

    from multiprocessing import Pool, cpu_count
    NCORES=cpu_count()

    def __setup(args):
        setup(*args)

    def __do(args):
        do(*args)

    do_jobs = []

    SQS = range(0,65,2)
    EQS = [0,]
    PSS = [NTRU_IMPROPER_HPS509, NTRU_IMPROPER_HPS677, NTRU_IMPROPER_HRSS701, NTRU_IMPROPER_HPS821]

    for (label, ps) in PSS:
        for i in SQS:
            for j in EQS:
                do_jobs.append((label, i, j))

    list(Pool(NCORES).imap_unordered(__setup, PSS))
    list(Pool(NCORES).imap_unordered(__do, do_jobs))
