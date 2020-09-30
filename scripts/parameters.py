from frodo import Frodo
from kyber import Kyber
from newhope import NewHope
from ntru import NTRUHPS, NTRUHRSS
from saber import Saber
from round5 import R5N1KEM0d, R5NDKEM0d

# Round 5, ring, cpa
R5ND1KEM0D = ("r2/r5nd1kem0d", R5NDKEM0d(618, 104, 1, 2**4, 2**8, 2**11))
R5ND3KEM0D = ("r2/r5nd3kem0d", R5NDKEM0d(786, 384, 1, 2**4, 2**9, 2**13))
R5ND5KEM0D = ("r2/r5nd5kem0d", R5NDKEM0d(1018, 428, 1, 2**4, 2**9, 2**14))
# Round 5, no ring, cpa
R5N11KEM0D = ("r2/r5n11kem0d", R5N1KEM0d(594, 7, 238, 3, 2**7, 2**10, 2**13))
R5N13KEM0D = ("r2/r5n13kem0d", R5N1KEM0d(881, 8, 238, 3, 2**7, 2**10, 2**13))
R5N15KEM0D = ("r2/r5n15kem0d", R5N1KEM0d(1186, 8, 712, 4, 2**7, 2**12, 2**15))
# Round 5, ring, cca
R5ND1PKE0D = ("r2/r5nd1pke0d", R5NDKEM0d(586, 182, 1, 2**4, 2**9, 2**13))
R5ND3PKE0D = ("r2/r5nd3pke0d", R5NDKEM0d(852, 212, 1, 2**5, 2**9, 2**12))
R5ND5PKE0D = ("r2/r5nd5pke0d", R5NDKEM0d(1170, 222, 1, 2**5, 2**9, 2**13))
# Round 5, no ring, cca
R5N11PKE0D = ("r2/r5n11pke0d", R5N1KEM0d(636, 8, 114, 2, 2**6, 2**9, 2**12))
R5N13PKE0D = ("r2/r5n13pke0d", R5N1KEM0d(876, 8, 446, 3, 2**7, 2**11, 2**15))
R5N15PKE0D = ("r2/r5n15pke0d", R5N1KEM0d(1217, 8, 462, 4, 2**9, 2**12, 2**15))
# Saber
LIGHTSABER = ("r2/lightsaber", Saber(256, 2, 5, 2**13, 2**10, 2**3))
SABER = ("r2/saber", Saber(256, 3, 4, 2**13, 2**10, 2**4))
FIRESABER = ("r2/firesaber", Saber(256, 4, 3, 2**13, 2**10, 2**6))
# Kyber round 1
KYBER512r1 = ("r1/kyber512", Kyber(256, 2, 5, 7681, 2**11, 2**11, 2**3))
KYBER768r1 = ("r1/kyber768", Kyber(256, 3, 4, 7681, 2**11, 2**11, 2**3))
KYBER1024r1 = ("r1/kyber1024", Kyber(256, 4, 3, 7681, 2**11, 2**11, 2**3))
# Kyber round 2
KYBER512r2 = ("r2/kyber512", Kyber(256, 2, 2, 3329, 2**12, 2**10, 2**3))
KYBER768r2 = ("r2/kyber768", Kyber(256, 3, 2, 3329, 2**12, 2**10, 2**4))
KYBER1024r2 = ("r2/kyber1024", Kyber(256, 4, 2, 3329, 2**12, 2**11, 2**5))
# Kyber round 3
KYBER512r3 = ("r3/kyber512", Kyber(256, 2, 3, 3329, 2**12, 2**10, 2**4, k2=2))
KYBER768r3 = ("r3/kyber768", Kyber(256, 3, 2, 3329, 2**12, 2**10, 2**4, k2=2))
KYBER1024r3 = ("r3/kyber1024", Kyber(256, 4, 2, 3329, 2**12, 2**11, 2**5, k2=2))
# Frodo
FRODO640 = ("r2/frodo640", Frodo(640, 8, 8, 2, 2**15))
FRODO976 = ("r2/frodo976", Frodo(976, 8, 8, 3, 2**16))
FRODO1344 = ("r2/frodo1344", Frodo(1344, 8, 8, 4, 2**16))
# Frodo High Failure
FRODO640Q13 = ("r2/frodo640q13", Frodo(640, 8, 8, 2, 2**13))
FRODO640Q14 = ("r2/frodo640q14", Frodo(640, 8, 8, 2, 2**14))
# NewHope
NEWHOPE512 = ("r2/newhope512", NewHope(512, 2, 8, 12289, 2**3))
NEWHOPE1024 = ("r2/newhope1024", NewHope(1024, 4, 8, 12289, 2**3))
NEWHOPE512q7681 = ("r2/newhope512q7681", NewHope(512, 2, 8, 7681, 2**3))
NEWHOPE1024q7681 = ("r2/newhope1024q7681", NewHope(1024, 4, 8, 7681, 2**3))
NEWHOPE512q3329 = ("r2/newhope512q3329", NewHope(512, 2, 4, 3329, 2**3))
# NTRU-HPS
NTRUEPHEM509 = ("r2/ntruephem509", NTRUHPS(509, 2048, ephem=True))
NTRUEPHEM677 = ("r2/ntruephem677", NTRUHPS(677, 2048, ephem=True))
NTRUEPHEM821 = ("r2/ntruephem821", NTRUHPS(821, 4096, ephem=True))
NTRUHPS509 = ("r2/ntruhps2048509", NTRUHPS(509, 2048, ephem=False))
NTRUHPS677 = ("r2/ntruhps2048677", NTRUHPS(677, 2048, ephem=False))
NTRUHPS821 = ("r2/ntruhps4096821", NTRUHPS(821, 4096, ephem=False))
# NTRU-HRSS
NTRUEPHEM701 = ("r2/ntruephem701", NTRUHRSS(701, ephem=True))
NTRUHPS821 = ("r2/ntruhrss701", NTRUHRSS(701, ephem=False))
