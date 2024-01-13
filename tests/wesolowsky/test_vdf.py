import unittest

from crypto_VDF.data_transfer_objects.dto import RsaSetup
from crypto_VDF.verifiable_delay_functions.wesolowski import WesolowskiVDF


class TestWesolowskiVDF(unittest.TestCase):

    def test_full_naive_vdf_completeness(self):
        security_parameter = 10
        delay = 4

        pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
        x = WesolowskiVDF.gen(pp)
        evaluation = WesolowskiVDF.eval_naive(setup=pp, input_param=x)
        verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof)
        self.assertTrue(verif)

    def test_full_naive_vdf_soundness(self):
        security_parameter = 128
        delay = 8

        pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
        x = WesolowskiVDF.gen(pp)
        evaluation = WesolowskiVDF.eval_naive(setup=pp, input_param=x)
        wrong_output = WesolowskiVDF.gen(pp)
        verif = WesolowskiVDF.verify(pp, x, wrong_output, evaluation.proof)
        self.assertFalse(verif)

    def test_full_vdf_completeness(self):
        security_parameter = 10
        delay = 4
        # Without trapdoor
        pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=False, delay=delay)
        x = WesolowskiVDF.gen(pp)
        evaluation = WesolowskiVDF.eval(setup=pp, input_param=x)
        verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof)
        self.assertTrue(verif)
        # # With trapdoor
        pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
        x = WesolowskiVDF.gen(pp)
        evaluation = WesolowskiVDF.trapdoor(setup=pp, input_param=x)
        verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof)
        self.assertTrue(verif)

    def test_full_vdf_completeness_2(self):
        security_parameter = 128
        delay = 1024
        # Without trapdoor
        # pp = WesolowskiVDF.setup(security_param=security_parameter, delay=delay)
        # x = WesolowskiVDF.gen(pp)
        # evaluation = WesolowskiVDF.eval(setup=pp, input_param=x)
        # verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof)
        # self.assertTrue(verif)
        # With trapdoor
        # pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
        # x = WesolowskiVDF.gen(pp)
        x = 15290776003867498194639638
        p_q = 260397651547576035527008437293696027923
        p_q_z = 260397651547576035494621789640204759480
        pp = RsaSetup(phi=p_q_z, n=p_q, delay=1048576, security_param=128)
        evaluation = WesolowskiVDF.trapdoor(setup=pp, input_param=x)
        verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof)
        self.assertTrue(verif)

    def test_full_vdf_soundness(self):
        security_parameter = 128
        delay = 8

        pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
        x = WesolowskiVDF.gen(pp)
        evaluation = WesolowskiVDF.eval(setup=pp, input_param=x)
        wrong_output = WesolowskiVDF.gen(pp)
        verif = WesolowskiVDF.verify(pp, x, wrong_output, evaluation.proof)
        self.assertFalse(verif)
