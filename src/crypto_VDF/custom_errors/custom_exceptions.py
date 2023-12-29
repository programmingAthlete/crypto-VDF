import pydantic


class BaseCaseException(Exception):
    name: str

    def __init__(self, message: str, name: str):
        self.name = name
        super().__init__(message)


class GeneralException(BaseCaseException):

    def __init__(self, name="GeneralException", message="General Exception"):
        super().__init__(name=name, message=message)


class PrimeNumberNotFound(BaseCaseException):

    def __init__(self, name="PrimeNumberGenerationFailed", message="Generation of prime number failed"):
        super().__init__(name=name, message=message)


class QuadraticResidueFailed(BaseCaseException):

    def __init__(self, name="QuadraticResidueGenerationFailed", message="Generation of quadratic residue failed"):
        super().__init__(name=name, message=message)


class NotAQuadraticResidueException(BaseCaseException):
    def __init__(self, name="NotAQuadraticResidue", message="The value is not a quadratic residue"):
        super().__init__(name=name, message=message)


class ValuesDivergenceException(pydantic.PydanticValueError):
    msg_template = "value {base_10} is not equal to the binary of {base_2} instead of {bin_base_10}"


class CoPrimeException(BaseCaseException):
    def __init__(self, name="IntegersAreNotCoPrimes", message="The integers are not co-primes"):
        super().__init__(name=name, message=message)
