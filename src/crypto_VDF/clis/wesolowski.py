from typing import Annotated

import typer
from orjson import orjson

from crypto_VDF.utils.logger import get_logger
from crypto_VDF.utils.utils import square_sequences_v2
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


@app.command(name="full-vdf2")
def cmd_full_vdf2(
        delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 2,
        security_parameter: Annotated[int, typer.Option(help="Bit lengths of the modulus")] = 10,
        verbose: Annotated[bool, typer.Option(help="Show Debug logs")] = False,
):
    pp = WesolowskiVDF.setup(security_param=security_parameter, ret_sk=True, delay=delay)
    print(f"Public parameters: {orjson.loads(pp.json())}\n")
    x = WesolowskiVDF.gen(pp)
    print(f"\nGenerated input: {x}\n")
    evaluation = WesolowskiVDF.eval_2(setup=pp, input_param=x, _verbose=verbose)
    print(f"\nGenerated output: {evaluation.output}")
    print(f"Generated Proof: {evaluation.proof}\n")
    verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof, verbose)
    print(f"\nVerification: {verif}")
    assert verif


@app.command(name="check-algo")
def cmd_check_alg(delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 2,
                  security_parameter: Annotated[int, typer.Option(help="Bit lengths of the modulus")] = 10,
                  ):
    pp = WesolowskiVDF.setup(security_param=security_parameter, delay=int(2 ** delay))
    # pp = RsaSetup(n=21, p=3, q=7, delay=4)
    g = WesolowskiVDF.gen(setup=pp)
    breakpoint()
    l = WesolowskiVDF.flat_shamir_hash(security_param=pp.delay, g=g, y=2)
    breakpoint()
    # verif = g ** (2 ** pp.delay // l) % pp.n
    alg_4 = WesolowskiVDF.alg_4_base(delay=pp.delay, prime_l=l, input_var=g, n=pp.n)
    # assert verif == alg_4[0]
    # self.assertEqual(verif, alg_4[0])
    breakpoint()
    out = square_sequences_v2(a=g, steps=pp.delay, n=pp.n)
    r = WesolowskiVDF.alg_4(n=pp.n, prime_l=l, delay=pp.delay, output_list=out[1])
    assert r == alg_4[0]
