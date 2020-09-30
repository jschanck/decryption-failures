def expectation(Pr, f=lambda x: x):
    return sum(f(x)*Pr[x] for x in Pr)

def expectation_of_convolution(P1, P2, f=lambda x: x):
    return sum(f(x+y)*P1[x]*P2[y] for x in P1 for y in P2)

def top_quantile(D, q):
    # Divides D = { x : Pr[x], ... } into q quantiles.
    # Returns conditional distribution of top quantile
    if q == 1:
        return D
    X = D.items()
    X = sorted(X, key=lambda x: x[0])
    i = len(X) - 1
    t = X[i][1]
    while i > 0 and (t + X[i-1][1] <= 1./q):
        i -= 1
        t += X[i][1]
    D2 = dict(X[i:])
    s = 1./sum(D2.values())
    for x in D2:
        D2[x] *= s
    return D2

def tail_probability(D, t):
    '''
    Probability that an drawn from D is strictly greater than t in absolute value
    :param D: Law (Dictionnary)
    :param t: tail parameter (integer)
    '''
    s = 0
    for (x,px) in sorted(D.items(), key=lambda t: abs(t[1])):
        if abs(x) > t:
            s += px
    return s

