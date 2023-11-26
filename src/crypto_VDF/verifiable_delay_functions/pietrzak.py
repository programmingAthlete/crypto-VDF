from crypto_VDF.verifiable_delay_functions.vdf import VDF


class PietrzakVDF(VDF):

    @classmethod
    def setup(cls, security_param, sequential_param):
        pass

    @classmethod
    def eval(cls, public_params):
        return cls.eval_function(public_params=public_params)

    @classmethod
    def verify(cls, public_params, input_param, output_param, proof=None):
        pass
