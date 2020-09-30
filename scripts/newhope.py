from mpmath import mp
from util import ZERO
from distributions import build_centered_binomial_dist,\
                          build_artifact_dist,\
                          dist_absolute,\
                          dist_convolution,\
                          dist_square,\
                          dist_product,\
                          dist_iter_convolution

NEWHOPE_APPROX_ZERO = mp.mpf(2**-600)

def dist_scale_newhope(A, x):
    B = {}
    for a in A:
        a2 = int(round(a * x + 0.5))
        B[a2] = B.get(a2, ZERO) + A[a]
    return B

def dist_cartesian_product(A, B):
    C = {}
    for a in A:
        for b in B:
            p = A[a] * B[b]
            a1 = a if isinstance(a,tuple) else (a,)
            b2 = b if isinstance(b,tuple) else (b,)
            c = a1+b2
            C[c] = p
    return C

def dist_negacyclic_sum(A):
    B = {}
    for a in A:
        c = [0]*len(a)
        for i in range(len(a)):
            for j in range(len(a)):
                s = -1 if j < i else 1
                c[j] += s * a[j-i]
        c = tuple(c)
        B[c] = B.get(c, ZERO) + A[a]
    return B

def dist_dot(A,B):
    C = {}
    for a in A:
        for b in B:
            c = sum([ai * bi for (ai,bi) in zip(a,b)])
            C[c] = C.get(c,ZERO) + A[a]*B[b]
    return C

class NewHope:
    def __init__(self, n, m, k, q, rc2):
        self.n = n
        self.m = m
        self.k = k
        self.q = q
        self.rc2 = rc2

        # TODO: document "Reduce" trick
        if self.m == 2:
            self.a = self.m**0.5
        elif self.m == 4:
            self.a = (1 + 6*self.k/self.n) * (self.m**0.5)
        else:
            raise ValueError("need m=2 or m=4")

        self.cache_dist_1 = None
        self.cache_dist_2 = None
        self.cache_dist_3 = None
        self.cache_dist_4 = None

    def rounds_pk(self):
        return False

    def rounds_c1(self):
        return False

    def rounds_c2(self):
        return self.rc2 < self.q

    def fixed_wt(self):
        return False

    def inner_product_dimension(self):
        return 2 * self.n

    def threshold(self):
        return self.m * self.q // 4

    def secret_l2_distribution(self):
        # Treat the secret key as a sample from the query
        # distribution scaled by self.a.
        if self.cache_dist_1 is None:
            D = self.query_l2_distribution()[0]
            D = dist_scale_newhope(D, self.a**2)
            self.cache_dist_1 = (D, D)
        return self.cache_dist_1

    def query_l2_distribution(self):
        if self.cache_dist_3 is None:
            c = build_centered_binomial_dist(self.k)
            D = dist_square(c)
            D = dist_iter_convolution(D, self.n, ignore_below=NEWHOPE_APPROX_ZERO)
            self.cache_dist_3 = (D, D)
        return self.cache_dist_3

    def e3_distribution(self):
        c = build_centered_binomial_dist(self.k)
        r = build_artifact_dist(self.q, self.rc2)
        D = dist_convolution(c, r)
        D = dist_iter_convolution(D, self.m, ignore_below=NEWHOPE_APPROX_ZERO)
        return D

    def one_shot_distribution(self):
        if self.cache_dist_2 is None:
            c = build_centered_binomial_dist(self.k)
            r = build_artifact_dist(self.q, self.rc2)
            D1 = dist_product(c, c)
            D1 = dist_iter_convolution(D1, 2*self.n, ignore_below=NEWHOPE_APPROX_ZERO)
            D1 = dist_scale_newhope(D1, self.a)
            D1 = dist_absolute(D1)
            D2 = dist_convolution(c, r)
            D2 = dist_iter_convolution(D2, self.m, ignore_below=NEWHOPE_APPROX_ZERO)
            D2 = dist_absolute(D2)
            D = dist_convolution(D1,D2)
            self.cache_dist_2 = D
        return self.cache_dist_2

    def one_shot_sllskn19(self):
        if self.cache_dist_4 is None:
            c = build_centered_binomial_dist(self.k)
            r = build_artifact_dist(self.q, self.rc2)
            cm = dist_cartesian_product(c,c)
            x = self.m//2
            while self.m > 1:
                cm = dist_cartesian_product(cm,cm)
                x //= 2
            cmsum = dist_negacyclic_sum(cm)
            W = dist_vector_dot(cm,cmsum)
            D1 = dist_iter_convolution(W, 2*self.n//self.m, ignore_below=NEWHOPE_APPROX_ZERO)
            D2 = dist_convolution(c, r)
            D2 = dist_iter_convolution(D2, self.m, ignore_below=NEWHOPE_APPROX_ZERO)
            D = dist_convolution(D1,D2)
            self.cache_dist_4 = D
        return self.cache_dist_4

