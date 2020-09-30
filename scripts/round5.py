from util import APPROX_ZERO
from distributions import build_artifact_dist,\
                          dist_convolution,\
                          dist_square,\
                          dist_negate,\
                          dist_iter_convolution

class R5NDKEM0d:
    def __init__(self, n, h, b, t, p, q):
        self.n = n
        self.h = h
        self.b = b
        self.t = t
        self.p = p
        self.q = q

        self.cache_dist_1 = None
        self.cache_dist_2 = None

    def rounds_pk(self):
        return self.p < self.q

    def rounds_c1(self):
        return self.p < self.q

    def rounds_c2(self):
        return self.t < self.q

    def fixed_wt(self):
        return True

    def inner_product_dimension(self):
        return 2 * self.n

    def threshold(self):
        return self.q // (2**(self.b+1))

    def secret_l2_distribution(self):
        if self.cache_dist_1 is None:
            D1 = build_artifact_dist(self.q, self.p)
            D1 = dist_convolution(D1, dist_negate(D1))
            D1 = dist_square(D1)
            D1 = dist_iter_convolution(D1, self.n)
            D2 = {self.h : 1.0}
            self.cache_dist_1 = (D1, D2)
        return self.cache_dist_1

    def query_l2_distribution(self):
        return self.secret_l2_distribution()[::-1]

    def e3_distribution(self):
        return build_artifact_dist(self.q, self.t)

    def one_shot_distribution(self):
        if self.cache_dist_2 is None:
            c = {1 : 0.5, -1 : 0.5}
            r1 = build_artifact_dist(self.q, self.p)
            r2 = build_artifact_dist(self.q, self.t)
            D = dist_convolution(c, r1)
            D = dist_iter_convolution(D, 4*self.h)
            D = dist_convolution(D, r2)
            self.cache_dist_2 = D
        return self.cache_dist_2


class R5N1KEM0d:
    def __init__(self, n, el, h, b, t, p, q):
        self.n = n
        self.el = el # m = el^2
        self.h = h
        self.b = b
        self.t = t
        self.p = p
        self.q = q

        self.cache_dist_1 = None
        self.cache_dist_2 = None

    def rounds_pk(self):
        return self.p < self.q

    def rounds_c1(self):
        return self.p < self.q

    def rounds_c2(self):
        return self.t < self.q

    def fixed_wt(self):
        return True

    def inner_product_dimension(self):
        return 2 * self.n

    def threshold(self):
        return self.q // (2**(self.b+1))

    def secret_l2_distribution(self):
        if self.cache_dist_1 is None:
            D1 = build_artifact_dist(self.q, self.p)
            D1 = dist_square(D1)
            D1 = dist_iter_convolution(D1, self.n)
            D2 = {self.h : 1.0}
            self.cache_dist_1 = (D1, D2)
        return self.cache_dist_1

    def query_l2_distribution(self):
        return self.secret_l2_distribution()[::-1]

    def e3_distribution(self):
        return build_artifact_dist(self.q, self.t)

    def one_shot_distribution(self):
        if self.cache_dist_2 is None:
            c = {1 : 0.5, -1 : 0.5}
            r1 = build_artifact_dist(self.q, self.p)
            r2 = build_artifact_dist(self.q, self.t)
            D = dist_convolution(c, r1)
            D = dist_iter_convolution(D, 2*self.h)
            D = dist_convolution(D, r2)
            self.cache_dist_2 = D
        return self.cache_dist_2
