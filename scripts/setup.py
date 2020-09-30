import pickle

from util import log2, jar, p, progress
from probabilities import tail_probability
from distributions import dist_absolute
from parameters import *

def setup(label, ps):
    progress(label, "starting setup")
    try:
        with open(jar(label), "rb") as brine:
            ps = pickle.load(brine)
    except IOError:
        progress(label, "generating distributions")

    secret_l2_dist = ps.secret_l2_distribution()
    progress(label, "done secret l2 dist")
    query_l2_dist = ps.query_l2_distribution()
    progress(label, "done query l2 dist")
    e3_dist = ps.e3_distribution()
    progress(label, "done e3 dist")
    one_shot_dist = ps.one_shot_distribution()
    progress(label, "done one shot dist")

    f = tail_probability(one_shot_dist, ps.threshold())
    p(label, "oneshot", float(-log2(f)))
    p(label, "max_abs_e3", max(dist_absolute(e3_dist)))

    with open(jar(label), "wb") as brine:
        pickle.dump(ps, brine)

    progress(label, "done setup")

if __name__ == "__main__":
    from multiprocessing import Pool, cpu_count

    NCORES=cpu_count()

    def __setup(args):
        setup(*args)

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

    list(Pool(NCORES).imap_unordered(__setup, PSS))

