from crypto_VDF.verifiable_delay_functions.vdf import VDF


class WesolowskiVDF(VDF):

    @classmethod
    def setup(cls, security_param, delay):
        pass

    @classmethod
    def eval(cls, public_params, input_param):
        return cls.eval_function(public_params=public_params, input_param=input_param)

    @classmethod
    def verify(cls, public_params, input_param: int, output_param: int, proof=None):
        pass
