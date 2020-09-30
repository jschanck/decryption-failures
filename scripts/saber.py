from distributions import build_centered_binomial_dist,\
                          build_artifact_dist,\
                          dist_convolution,\
                          dist_square,\
                          dist_product,\
                          dist_iter_convolution

class Saber:
    def __init__(self, n, m, k, q, p, T):
        self.n = n
        self.m = m
        self.k = k
        self.q = q
        self.p = p
        self.T = T

        self.cache_dist_1 = None
        self.cache_dist_2 = None

    def rounds_pk(self):
        return self.p < self.q

    def rounds_c1(self):
        return self.p < self.q

    def rounds_c2(self):
        return self.T < self.q

    def fixed_wt(self):
        return False

    def inner_product_dimension(self):
        return 2 * self.m * self.n

    def threshold(self):
        return self.q // 4

    def secret_l2_distribution(self):
        if self.cache_dist_1 is None:
            # b = <A*s2>_{q->p}.
            # s1 is rounding noise
            r = build_artifact_dist(self.q, self.p)
            S1 = dist_square(r)
            S1 = dist_iter_convolution(S1, self.m * self.n)
            # s2 is centered binomial
            c = build_centered_binomial_dist(self.k)
            S2 = dist_square(c)
            S2 = dist_iter_convolution(S2, self.m * self.n)
            self.cache_dist_1 = (S1, S2)
        return self.cache_dist_1

    def query_l2_distribution(self):
        return self.secret_l2_distribution()[::-1]

    def e3_distribution(self):
        return build_artifact_dist(self.q, self.T)

    def one_shot_distribution(self):
        if self.cache_dist_2 is None:
            c = build_centered_binomial_dist(self.k)
            r = build_artifact_dist(self.q, self.p)
            cr = dist_product(c, r)
            D = dist_iter_convolution(cr, 2 * self.m * self.n)
            D = dist_convolution(D, self.e3_distribution())
            self.cache_dist_2 = D
        return self.cache_dist_2
