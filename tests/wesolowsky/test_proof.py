import unittest

from crypto_VDF.data_transfer_objects.dto import RsaSetup
from crypto_VDF.utils.utils import square_sequences_v2
from crypto_VDF.verifiable_delay_functions.wesolowski import WesolowskiVDF


class TestWesolowskiProof(unittest.TestCase):

    def test_alg_4(self):
        sec_param = 10
        delay = 4

        pp = WesolowskiVDF.setup(security_param=sec_param, delay=delay)
        x = WesolowskiVDF.gen(pp)

        y = square_sequences_v2(steps=pp.delay, a=x, n=pp.n)
        prime_l = WesolowskiVDF.flat_shamir_hash(security_param=pp.security_param, g=x, y=y[0])
        proof = WesolowskiVDF.alg_4(n=pp.n, prime_l=prime_l, delay=pp.delay, output_list=y[1])
        e = 2**pp.delay
        exp = e // prime_l
        t = (x**(exp)) % pp.n

        al4 = WesolowskiVDF.alg_4_base(delay=pp.delay, prime_l=prime_l, input_var=x, n=pp.n)
        a = 1

    def test_a(self):
        # al4 = WesolowskiVDF.alg_4_base(delay=4, prime_l=5, input_var=3, n=21)
        # pp = WesolowskiVDF.setup(security_param=6, delay=4)
        # y = square_sequences_v2(steps=4, a=3, n=21)
        # proof = WesolowskiVDF.alg_4(n=21, prime_l=5, delay=pp.delay, output_list=y[1])
        # verif = 2**4 // 5
        # self.assertEqual(al4[0], 3**verif % 21)

        pp = RsaSetup(n=21, p=3, q=7, delay=4)
        g = WesolowskiVDF.gen(setup=pp)

        l = WesolowskiVDF.flat_shamir_hash(security_param=4, g=g, y=2)
        g = 5
        verif = g**(2**4 // l) % pp.n
        alg_4 = WesolowskiVDF.alg_4_base(delay=pp.delay, prime_l=l, input_var=g, n=21)

        a_4 = WesolowskiVDF.alg_4(n=pp.n, prime_l=l, delay=pp.delay, output_list=alg_4[1])
        a = 1
        # 0 0 1 1

    def test_alg_4_base(self):
        # pp = WesolowskiVDF.setup(security_param=100, delay=2**8)
        # pp = RsaSetup(n=21, p=3, q=7, delay=4)
        # for i in range(10):
        #     g = WesolowskiVDF.gen(setup=pp)
        #
        #     l = WesolowskiVDF.flat_shamir_hash(security_param=pp.delay, g=g, y=2)
        #     verif = g ** (2 ** pp.delay // l) % pp.n
        #     alg_4 = WesolowskiVDF.alg_4_base(delay=pp.delay, prime_l=l, input_var=g, n=pp.n)
        #     # self.assertEqual(verif, alg_4[0])
        #     out = square_sequences_v2(a=g, steps=pp.delay, n=pp.n)
        #     r = WesolowskiVDF.alg_4(n=pp.n, prime_l=l, delay=pp.delay, output_list=out[1])
        #     self.assertEqual(r, alg_4[0])

        pp = WesolowskiVDF.setup(security_param=100, delay=int(2**8))
        # pp = RsaSetup(n=21, p=3, q=7, delay=4)
        g = WesolowskiVDF.gen(setup=pp)

        l = WesolowskiVDF.flat_shamir_hash(security_param=pp.delay, g=g, y=2)
        verif = g ** (2 ** pp.delay // l) % pp.n
        alg_4 = WesolowskiVDF.alg_4_base(delay=pp.delay, prime_l=l, input_var=g, n=pp.n)
        # self.assertEqual(verif, alg_4[0])
        out = square_sequences_v2(a=g, steps=pp.delay, n=pp.n)
        r = WesolowskiVDF.alg_4(n=pp.n, prime_l=l, delay=pp.delay, output_list=out[1])
        self.assertEqual(r, alg_4[0])

    def test_2(self):
        g = 5
        l = 13
        n = 21
        t = 4
        alg_4 = WesolowskiVDF.alg_4_base(delay=t, prime_l=l, input_var=g, n=n)
        v = g**(2**t // l) % n
        self.assertEqual(alg_4[0], v)
        out = square_sequences_v2(a=g, steps=t, n=n)
        r = WesolowskiVDF.alg_4(n=n, prime_l=l, delay=t, output_list=out[1])
        self.assertEqual(r, alg_4[0])






