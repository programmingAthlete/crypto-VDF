import logging
from typing import Annotated

import typer
from orjson import orjson

from crypto_VDF.custom_errors.custom_exceptions import NotAQuadraticResidueException
from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.utils.logger import get_logger
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)


_log = get_logger(__name__)


@app.command(name="full-vdf")
def cmd_full_vdf(
        delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 2,
        security_parameter: Annotated[int, typer.Option(help="Bit lengths of the modulus")] = 10
):
    pp = PietrzakVDF.setup(security_param=security_parameter, delay=delay)
    print(f"Public parameters: {orjson.loads(pp.json())}\n")
    x = PietrzakVDF.gen(pp)
    print(f"\nGenerated input: {x}\n")
    output, proof = PietrzakVDF.eval(public_params=pp, input_param=x)
    print(f"\nGenerated output: {x}")
    print(f"Generated Proof: {proof}\n")
    verif = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=output, proof=proof)
    print(f"\nVerification: {verif}")
    assert verif


# x = 10 11
@app.command(name='generate-and-verify')
def cmd_generate_and_verify(x: Annotated[int, typer.Argument(help="Input to the VDF")],
                            delay: Annotated[int, typer.Option(help="Delay parameter of the VDF")] = 2,
                            modulus: Annotated[int, typer.Option(help="Modulus of the Zn")] = 21,
                            verbose: Annotated[bool, typer.Option(help="Show Debug Logs")] = False):
    pp = PublicParams(modulus=modulus, delay=delay)
    print(f"\nGenerated the public parameters: {orjson.loads(pp.json())}\n")
    output = PietrzakVDF.sol(input_param=x, public_params=pp)
    print(f"\nProduced the output {output}\n")
    proof = PietrzakVDF.compute_proof(public_params=pp, input_param=x, log=verbose)
    print(f"\nProduced the proof: {proof}\n")
    verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=output, log=verbose, proof=proof)
    print(f"\nVerification: {verification}")
    assert verification


# out 16384 delay 6 modulus 21
@app.command(name='proof')
def cmd_proof(
        x: Annotated[int, typer.Argument(help="Input to the VDF")],
        y: Annotated[int, typer.Argument(help="Output to the VDF")],
        delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 1,
        modulus: Annotated[int, typer.Option(help="Modulus of the Zn")] = 21,
        verbose: Annotated[bool, typer.Option(help="Show Debug Logs")] = False):
    pp = PublicParams(modulus=modulus, delay=delay)
    out = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=y, log=verbose)
    print(out)


# x 13
@app.command(name='output')
def cmd_sol(
        x: Annotated[int, typer.Argument(help="Input to the VDF")],
        delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 1,
        modulus: Annotated[int, typer.Option(help="Modulus of the Zn")] = 21):
    pp = PublicParams(modulus=modulus, delay=delay)
    out = PietrzakVDF.sol(input_param=x, public_params=pp)
    print(out)


@app.command(name='verify')
def cmd_verif(x: int = 16384, y: int = 6, delay: int = 1, modulus: int = 21, log: bool = False):
    pp = PublicParams(modulus=modulus, delay=delay)
    proof = [16]
    out = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=y, proof=proof, log=log)
    print(out)


@app.command(name="eval")
def cmd_eval(security_parameter: int = 8, delay: int = 6):
    pp = PietrzakVDF.setup(security_param=security_parameter, delay=delay)
    x = PietrzakVDF.gen(pp)
    y = PietrzakVDF.eval(public_params=pp, input_param=x)
    print("Output of Eval:", y)


@app.command(name="setup")
def cmd_setup(security_parameter: int = 100, delay: int = 100):
    pp = PietrzakVDF.setup(security_param=security_parameter, delay=delay)
    print(f"{orjson.loads(pp.json())}")


@app.command(name="gen")
def cmd_gen(delay: int = 100, modulus: int = 100):
    pp = PublicParams(delay=delay, modulus=modulus)
    x = PietrzakVDF.gen(pp)
    print(f"Generated quadratic residue: {x}")


@app.command(name="eval-function")
def cmd_eval_function(x: int, delay: int = 100, modulus: int = 100):
    if not NumberTheory.check_quadratic_residue(x=x, modulus=modulus):
        raise NotAQuadraticResidueException(message=f'The value {x} is not a quadratic residue')
    pp = PublicParams(delay=delay, modulus=modulus)
    y = PietrzakVDF.eval_function(public_params=pp, input_param=x)
    print("Output of Eval:", y)
