import unittest

from crypto_VDF.verifiable_delay_functions.wesolowski import WesolowskiVDF


class TestWesolowskiVDF(unittest.TestCase):

    def test_full_vdf_completeness(self):
        security_parameter = 10
        delay = 4

        pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
        x = WesolowskiVDF.gen(pp)
        evaluation = WesolowskiVDF.eval_2(setup=pp, input_param=x)
        verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof)
        self.assertTrue(verif)

    def test_full_vdf_soundness(self):
        security_parameter = 128
        delay = 8

        pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
        x = WesolowskiVDF.gen(pp)
        evaluation = WesolowskiVDF.eval_2(setup=pp, input_param=x)
        wrong_output = WesolowskiVDF.gen(pp)
        verif = WesolowskiVDF.verify(pp, x, wrong_output, evaluation.proof)
        self.assertFalse(verif)
