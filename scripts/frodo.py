from distributions import dist_convolution,\
                          dist_square,\
                          dist_product,\
                          dist_iter_convolution

def dist_frodo(n):
    if n == 640:
        T = [9288, 8720, 7216, 5264, 3384, 1918, 958, 422, 164, 56, 17, 4, 1]
    elif n == 976:
        T = [11278, 10277, 7774, 4882, 2545, 1101, 396, 118, 29, 6, 1]
    elif n == 1344:
        T = [18286, 14320, 6876, 2023, 364, 40, 2]
    else:
        raise ValueError("Unsupported n")
    D = {}
    for (i, j) in enumerate(T):
        D[i] = 2**-16 * j
        D[-i] = 2**-16 * j
    return D

class Frodo:
    def __init__(self, n, nbar, mbar, B, q):
        self.n = n
        self.nbar = nbar
        self.mbar = mbar
        self.B = B
        self.q = q
        self.cache_dist_1 = None
        self.cache_dist_2 = None

    def rounds_pk(self):
        return False

    def rounds_c1(self):
        return False

    def rounds_c2(self):
        return False

    def fixed_wt(self):
        return False

    def inner_product_dimension(self):
        return 2 * self.n

    def threshold(self):
        return self.q // (2 * 2**self.B)

    def secret_l2_distribution(self):
        if self.cache_dist_1 is None:
            coeff = dist_frodo(self.n)
            D = dist_square(coeff)
            D = dist_iter_convolution(D, self.n)
            self.cache_dist_1 = (D, D)
        return self.cache_dist_1

    def query_l2_distribution(self):
        return self.secret_l2_distribution()

    def e3_distribution(self):
        return dist_frodo(self.n)

    def one_shot_distribution(self):
        if self.cache_dist_2 is None:
            s = dist_frodo(self.n)
            D = dist_product(s, s)
            D = dist_iter_convolution(D, 2 * self.n)
            D = dist_convolution(D, s)
            self.cache_dist_2 = D
        return self.cache_dist_2
