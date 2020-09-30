from distributions import build_centered_binomial_dist,\
                          build_artifact_dist,\
                          dist_convolution,\
                          dist_square,\
                          dist_product,\
                          dist_iter_convolution

class Kyber:
    def __init__(self, n, m, k, q, r0, r1, r2, k2=None):
        self.n = n
        self.m = m
        self.k = k
        self.k2 = k2
        self.q = q
        self.r0 = r0
        self.r1 = r1
        self.r2 = r2

        self.cache_dist_1 = None
        self.cache_dist_2 = None
        self.cache_dist_3 = None

    def rounds_pk(self):
        return self.r0 < self.q

    def rounds_c1(self):
        return self.r1 < self.q

    def rounds_c2(self):
        return self.r2 < self.q

    def fixed_wt(self):
        return False

    def inner_product_dimension(self):
        return 2 * self.m * self.n

    def threshold(self):
        return self.q // 4

    def secret_l2_distribution(self):
        # b = <s1 - A*s2>_{q -> r0}
        # s1 is cbd + r0 rounding
        # s2 is cbd
        if self.cache_dist_1 is None:
            c = build_centered_binomial_dist(self.k)
            r = build_artifact_dist(self.q, self.r0)
            S1 = dist_convolution(c, r)
            S1 = dist_square(S1)
            S1 = dist_iter_convolution(S1, self.m * self.n)
            S2 = dist_square(c)
            S2 = dist_iter_convolution(S2, self.m * self.n)
            self.cache_dist_1 = (S1, S2)
        return self.cache_dist_1

    def query_l2_distribution(self):
        # c1 = <e1A + e2>_{q -> r1}
        # e1 is cbd
        # e2 is cbd + r1 rounding
        if self.r0 == self.r1:
            return self.secret_l2_distribution()[::-1]
        if self.cache_dist_2 is None:
            c = build_centered_binomial_dist(self.k)
            r = build_artifact_dist(self.q, self.r1)
            E1 = dist_square(c)
            E1 = dist_iter_convolution(E1, self.m * self.n)
            if self.k2:
                c2 = build_centered_binomial_dist(self.k2)
            else:
                c2 = c
            E2 = dist_convolution(c2, r)
            E2 = dist_square(E2)
            E2 = dist_iter_convolution(E2, self.m * self.n)
            self.cache_dist_2 = (E1, E2)
        return self.cache_dist_2

    def e3_distribution(self):
        # c2 = <e1b + e3>_{q -> r2}
        # e3 is cbd + r2 rounding
        c = build_centered_binomial_dist(self.k2 if self.k2 else self.k)
        r = build_artifact_dist(self.q, self.r2)
        E3 = dist_convolution(c, r)
        return E3

    def one_shot_distribution(self):
        if self.cache_dist_3 is None:
            k1 = build_centered_binomial_dist(self.k)
            k2 = build_centered_binomial_dist(self.k2 if self.k2 else self.k)
            r0 = build_artifact_dist(self.q, self.r0)
            r1 = build_artifact_dist(self.q, self.r1)
            r2 = build_artifact_dist(self.q, self.r2)
            k1Pr0 = dist_convolution(k1, r0)
            k2Pr1 = dist_convolution(k2, r1)
            k2Pr2 = dist_convolution(k2, r2)
            D1 = dist_product(k1, k1Pr0)
            D2 = dist_product(k1, k2Pr1)
            D = dist_convolution(D1, D2)
            D = dist_iter_convolution(D, self.m * self.n)
            D = dist_convolution(D, k2Pr2)
            self.cache_dist_3 = D
        return self.cache_dist_3
