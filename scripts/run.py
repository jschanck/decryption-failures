import pickle

from mpmath import mp
from util import log2, jar, p, progress, APPROX_ZERO
from probabilities import expectation, \
                          expectation_of_convolution, \
                          top_quantile, \
                          tail_probability
from distributions import dist_convolution, dist_scale
from volume_estimate import volume_estimate
from parameters import *

def condition_on_quantiles(label, ps, sq, eq):
    # Spend more time searching for big s1 and e2 if the parameter set
    # uses fixed weight s2 and e1.
    sq1 = sq if not ps.fixed_wt() else sq**2
    sq2 = sq if not ps.fixed_wt() else 1
    eq1 = eq if not ps.fixed_wt() else 1
    eq2 = eq if not ps.fixed_wt() else eq**2

    secret_l2_dist = ps.secret_l2_distribution()
    query_l2_dist = ps.query_l2_distribution()

    S1 = top_quantile(secret_l2_dist[0], sq1)
    p(label, "s1/{}/min".format(round(log2(sq1))), min(S1))

    S2 = top_quantile(secret_l2_dist[1], sq2)
    p(label, "s2/{}/min".format(round(log2(sq2))), min(S2))

    E1 = top_quantile(query_l2_dist[0], eq1)
    p(label, "e1/{}/min".format(round(log2(eq1))), min(E1))

    E2 = top_quantile(query_l2_dist[1], eq2)
    p(label, "e2/{}/min".format(round(log2(eq2))), min(E2))

    # Swap first components for Round5, Saber, Kyber round 1
    if ps.rounds_pk() and ps.rounds_c1():
        # [s1 + t1][e1     ] <- [e1][s1 + t1]
        # [s2     ][e2 + t2] <- [s2][e2 + t2]
        [S1, E1, S2, E2] = [E1, S1, S2, E2]

    # Scale e1,e2 for spherical symmetry
    # [s1][e1] <- [s1 * 1/Z][e1 * Z  ]
    # [s2][e2] <- [s2 * Z  ][e2 * 1/Z]
    Z = mp.sqrt(expectation(E2) / expectation(E1))
    S1 = dist_scale(S1, 1/Z)
    S2 = dist_scale(S2, Z)
    E1 = dist_scale(E1, Z)
    E2 = dist_scale(E2, 1/Z)

    alpha = expectation_of_convolution(S1, S2)
    Q = dist_convolution(E1, E2, ignore_below=APPROX_ZERO)
    return (alpha, Q)


def do(label, lgsq, lgeq):
    with open(jar(label), "rb") as brine:
        ps = pickle.load(brine)

    progress(label, "starting s/{}/e/{}".format(lgsq, lgeq))
    (alpha, Q) = condition_on_quantiles(label, ps, 2**lgsq, 2**lgeq)

    e3_dist = ps.e3_distribution()
    cost, e3_cutoff = volume_estimate(ps, Q, alpha)
    p(label, "s/{}/e/{}/cost".format(lgsq, lgeq), float(cost))
    p(label, "s/{}/e/{}/e3/cutoff".format(lgsq, lgeq), int(e3_cutoff))
    p(label, "s/{}/e/{}/e3/cost".format(lgsq, lgeq), float(-log2(tail_probability(e3_dist, e3_cutoff-1))))
    progress(label, "done s/{}/e/{}".format(lgsq, lgeq))


if __name__ == "__main__":
    from multiprocessing import Pool, cpu_count

    NCORES=cpu_count()

    def __do(args):
        do(*args)

    do_jobs = []

    SQS = [1,]
    EQS = range(65)
    PSS = [
           R5ND1KEM0D  , R5ND3KEM0D   , R5ND5KEM0D  , \
           R5N11KEM0D  , R5N13KEM0D   , R5N15KEM0D  , \
           R5ND1PKE0D  , R5ND3PKE0D   , R5ND5PKE0D  , \
           R5N11PKE0D  , R5N13PKE0D   , R5N15PKE0D  , \
           LIGHTSABER  , SABER        , FIRESABER   , \
           KYBER512r1  , KYBER768r1   , KYBER1024r1 , \
           KYBER512r2  , KYBER768r2   , KYBER1024r2 , \
           KYBER512r3  , KYBER768r3   , KYBER1024r3 , \
           FRODO640    , FRODO976     , FRODO1344   , \
           FRODO640Q13 , FRODO640Q14  , \
           NEWHOPE512  , NEWHOPE1024  , \
          ]

    for (label, ps) in PSS:
        for i in SQS:
            for j in EQS:
                do_jobs.append((label, i, j))

    list(Pool(NCORES).imap_unordered(__do, do_jobs))
