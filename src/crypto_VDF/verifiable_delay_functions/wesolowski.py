from crypto_VDF.verifiable_delay_functions.vdf import VDF


class WesolowskiVDF(VDF):

    @classmethod
    def setup(cls, security_param, sequential_param):
        pass

    @classmethod
    def eval(cls, public_params):
        return VDF.eval_function(public_params=public_params)

    @classmethod
    def verify(cls, public_params, input_param: int, output_param: int, proof=None):
        pass
