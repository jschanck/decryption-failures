from util import binomial, mod_switch, mod_centered, ZERO, APPROX_ZERO

def dist_absolute(A):
    C = {}
    for a in A:
        c = abs(a)
        C[c] = C.get(c, ZERO) + A[a]
    return C

def dist_clean(A):
    """ Clean a distribution to accelerate further computation (drop element of the support with proba less than 2^-300)
    :param A: input law (dictionnary)
    """
    B = {}
    for (x, y) in A.items():
        if y > APPROX_ZERO:
            B[x] = y
    return B

def dist_convolution(A, B, ignore_below=ZERO):
    """ Construct the convolution of two laws (sum of independent variables from two input laws)
    :param A: first input law (dictionnary)
    :param B: second input law (dictionnary)
    """
    C = {}
    for a in A:
        for b in B:
            p = A[a] * B[b]
            if (p > ignore_below):
                C[a+b] = C.get(a+b, ZERO) + p
    return C

def dist_iter_convolution(A, i, ignore_below=APPROX_ZERO):
    """ compute the -ith forld convolution of a distribution (using double-and-add)
    :param A: first input law (dictionnary)
    :param i: (integer)
    """
    D = {0: 1.0}
    i_bin = bin(i)[2:]  # binary representation of n
    for ch in i_bin:
        D = dist_convolution(D, D, ignore_below=ignore_below)
        if ch == '1':
            D = dist_convolution(D, A, ignore_below=ignore_below)
    return D

def dist_mod(A, p):
    B = {}
    for a in A:
        B[a % p] = B.get(a % p, ZERO) + A[a]
    return B

def dist_product(A, B):
    """ Construct the law of the product of independent variables from two input laws
    :param A: first input law (dictionnary)
    :param B: second input law (dictionnary)
    """
    C = {}
    for a in A:
        for b in B:
            c = a*b
            C[c] = C.get(c, ZERO) + A[a] * B[b]
    return C

def dist_negate(A):
    B = {}
    for a in A:
        B[-a] = A[a]
    return B

def dist_scale(A, c):
    """ XXX: not general. Assumes A has integer keys and rounds a*c to the first decimal place. """
    B = {}
    for a in A:
        B[round(10 * a * c)/10] = A[a]
    return B

def dist_square(A):
    C = {}
    for a in A:
        c = a*a
        C[c] = C.get(c, ZERO) + A[a]
    return C

def build_artifact_dist(q, rq):
    """ Construct Error distribution: distribution of the difference introduced by switching from and back a uniform value mod q
    :param q: original modulus (integer)
    :param rq: intermediate modulus (integer)
    """
    D = {}
    for x in range(q):
        y = mod_switch(x, q, rq)
        z = mod_switch(y, rq, q)
        d = mod_centered(x - z, q)
        D[d] = D.get(d, ZERO) + 1./q

    return D

def build_centered_binomial_dist(k):
    """ Construct the binomial distribution as a dictionnary
    :param k: (integer)
    :param x: (integer)
    :returns: A dictionnary {x:p_k(x) for x in {-k..k}}
    """
    D = {}
    for i in range(0, k+1):
        D[i] = D[-i] = binomial(2*k, i+k) / 2.**(2*k)
    return D
