import unittest

from crypto_VDF.data_transfer_objects.dto import RsaSetup, EvalResponse
from crypto_VDF.utils.utils import exp_modular
from crypto_VDF.verifiable_delay_functions.wesolowski import WesolowskiVDF


class TestTrapdoor(unittest.TestCase):

    def test_trapdoor(self):
        p_q = 260397651547576035527008437293696027923
        p_q_z = 260397651547576035494621789640204759480

        # x = 152907760038674981946396383114530074665
        x = 15290776003867498194639638

        pp = RsaSetup(phi=p_q_z, n=p_q, delay=1048576, security_param=128)
        t = WesolowskiVDF.trapdoor(input_param=x, setup=pp)
        self.assertTrue(isinstance(t, EvalResponse))
        self.assertEqual(t.output, 168141932168425576701990652760156326268)
        self.assertTrue(t.proof < pp.n)
        prime_l = WesolowskiVDF.flat_shamir_hash(security_param=pp.security_param, g=x, y=t.output)
        r = exp_modular(a=2, exponent=pp.delay, n=prime_l)
        v = (exp_modular(a=t.proof, exponent=prime_l, n=pp.n) * exp_modular(a=x, exponent=r, n=pp.n)) % pp.n
        self.assertEqual(v, t.output)
