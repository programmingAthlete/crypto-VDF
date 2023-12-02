import typer
from orjson import orjson

from crypto_VDF.custom_errors.custom_exceptions import NotAQuadraticResidueException
from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.utils.number_theory import NumberTheory
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)


# out 16384 delay 6 modulus 21
@app.command(name='proof')
def cmd_proof(x: int = 10, y: int = 16, delay: int = 1, modulus: int = 21, log: bool = False):
    pp = PublicParams(modulus=modulus, delay=delay)
    out = PietrzakVDF.compute_proof(public_params=pp, input_param=x, output_param=y, log=log)
    print(out)


# x 13
@app.command(name='output')
def cmd_sol(x: int = 13, delay: int = 1, modulus: int = 21):
    pp = PublicParams(modulus=modulus, delay=delay)
    out = PietrzakVDF.sol(input_param=x, public_params=pp)
    print(out)


@app.command(name='verify')
def cmd_verif(x: int = 16384, y: int = 6, delay: int = 1, modulus: int = 21, log: bool = False):
    pp = PublicParams(modulus=modulus, delay=delay)
    proof = [16, 1, 16420, 16430, 16438, 16454]
    proof = [10]
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
