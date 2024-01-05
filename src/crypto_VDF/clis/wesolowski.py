from typing import Annotated

import typer
from orjson import orjson

from crypto_VDF.utils.logger import get_logger
from crypto_VDF.verifiable_delay_functions.wesolowski import WesolowskiVDF

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)

_log = get_logger(__name__)


@app.command(name="full-vdf")
def cmd_full_vdf(
        delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 2,
        security_parameter: Annotated[int, typer.Option(help="Bit lengths of the modulus")] = 10,
        trapdoor: Annotated[bool, typer.Option(help="Use trapdoor")] = False,
        verbose: Annotated[bool, typer.Option(help="Show Debug logs")] = False,
):
    pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
    print(f"Public parameters: {orjson.loads(pp.json())}\n")
    x = WesolowskiVDF.gen(pp)
    print(f"\nGenerated input: {x}\n")
    if trapdoor:
        print(f"Running Trapdoor with sk {pp.phi}\n")
        evaluation = WesolowskiVDF.trapdoor(setup=pp, input_param=x)
    else:
        print("Running Evaluation\n")
        evaluation = WesolowskiVDF.eval(setup=pp, input_param=x, _verbose=verbose)
    print(f"\nGenerated output: {evaluation.output}")
    print(f"Generated Proof: {evaluation.proof}\n")
    verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof, verbose)
    print(f"\nVerification: {verif}")
    assert verif
