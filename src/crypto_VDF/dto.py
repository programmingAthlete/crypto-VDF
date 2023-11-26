from typing import List


class KBitPrimeResponse:

    def __init__(self, status: bool, base_10, base_2: List[int]):
        self.status = status
        validation = self.validate(base_10, base_2)
        self.base_10 = validation.get("base_10")
        self.base_2 = validation.get("base_2")

    def validate(self, base_10, base_2):
        if len(base_2) == 1 and base_10 or len(base_2) > 0 and not base_2:
            raise Exception("FormatError")
        if self.status and not base_10:
            raise Exception("FormatError")
        return {"base_2": base_2, "base_10": base_10}


class GeneratePrimesResponse:

    def __init__(self, p: KBitPrimeResponse, q: KBitPrimeResponse):
        self.p = p
        self.q = q


class PublicParams:

    def __init__(self, delay: int, modulus: int):
        self.delay = delay
        self.modulus = modulus
