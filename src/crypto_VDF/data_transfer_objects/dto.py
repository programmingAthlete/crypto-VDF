from typing import List, Optional

import pydantic
from pydantic import root_validator

from crypto_VDF.custom_errors.custom_exceptions import ValuesDivergenceException


class KBitPrimeResponse(pydantic.BaseModel):
    base_10: int
    base_2: List[int]

    @root_validator(pre=False)
    def validate_base_10_and_2(cls, values):
        if len(values.get('base_2')) == 0:
            raise ValuesDivergenceException(base_10=values.get('base_10'),
                                            bin_base_10=bin(values.get('base_10'))[2:],
                                            base_2='')
        if values.get('base_2') != [int(item) for item in bin(values.get('base_10'))[2:]]:
            raise ValuesDivergenceException(base_10=values.get('base_10'),
                                            bin_base_10=bin(values.get('base_10'))[2:],
                                            base_2=''.join([str(item) for item in values.get('base_2')]))
        return values


class GeneratePrimesResponse(pydantic.BaseModel):
    p: KBitPrimeResponse
    q: KBitPrimeResponse


class PublicParams(pydantic.BaseModel):
    delay: int
    modulus: int
    security_param: Optional[int]
