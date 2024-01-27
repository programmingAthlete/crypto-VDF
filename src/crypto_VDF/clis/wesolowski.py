from typing import Annotated

import typer
from orjson import orjson

from crypto_VDF.data_transfer_objects.plotter import InputType
from crypto_VDF.plotter.wesolowski_grapher import WesolowskiGrapher
from crypto_VDF.utils.logger import get_logger
from crypto_VDF.utils.utils import square_sequences_v2
from crypto_VDF.verifiable_delay_functions.wesolowski import WesolowskiVDF
import pandas as pd
from time import time as t, strftime, gmtime

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)

_log = get_logger(__name__)


@app.command(name="full-vdf-naive")
def cmd_full_naive_vdf(
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
        evaluation = WesolowskiVDF.eval_naive(setup=pp, input_param=x, _verbose=verbose)
    print(f"\nGenerated output: {evaluation.output}")
    print(f"Generated Proof: {evaluation.proof}\n")
    verif = WesolowskiVDF.verify(pp, x, evaluation.output, evaluation.proof, verbose)
    print(f"\nVerification: {verif}")
    assert verif


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


@app.command(name="check-algo")
def cmd_check_alg(delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 2,
                  security_parameter: Annotated[int, typer.Option(help="Bit lengths of the modulus")] = 10,
                  ):
    pp = WesolowskiVDF.setup(security_param=security_parameter, delay=int(2 ** delay))
    # pp = RsaSetup(n=21, p=3, q=7, delay=4)
    g = WesolowskiVDF.gen(setup=pp)
    prime_l = WesolowskiVDF.flat_shamir_hash(security_param=pp.delay, g=g, y=2)
    # verif = g ** (2 ** pp.delay // l) % pp.n
    alg_4 = WesolowskiVDF.alg_4_original(delay=pp.delay, prime_l=prime_l, input_var=g, n=pp.n)
    out = square_sequences_v2(a=g, steps=pp.delay, n=pp.n)
    r = WesolowskiVDF.alg_4_revisited(n=pp.n, prime_l=prime_l, delay=pp.delay, output_list=out[1])
    assert r == alg_4[0]


@app.command(name="plots")
def cmd_complexity_plots(
        max_delay_exp: Annotated[int, typer.Option(help="Maximum exponent of delay")] = 20,
        iterations: Annotated[int, typer.Option(help="Number of iterations")] = 10,
        fix_input: Annotated[bool, typer.Option(help="Run with fixed input")] = False,
        store_measurements: Annotated[bool, typer.Option(help="Store the measurement")] = True,
        re_measure: Annotated[
            bool, typer.Option(help="Re-run the VDF instead of using past measurement to plot")] = True,
        show: Annotated[bool, typer.Option(help="Show the plot")] = False,
        verbose: Annotated[bool, typer.Option(help="Show Debug Logs")] = False
):
    s = t()
    input_type = InputType.RANDOM_INPUT if fix_input is False else InputType.FIX_INPUT
    grapher = WesolowskiGrapher(number_of_delays=max_delay_exp, number_ot_iterations=iterations, input_type=input_type)
    title = f"Wesolowski VDF complexity (mean after {grapher.number_ot_iterations} iterations)"
    if re_measure is False and not grapher.paths.macrostate_file_name.is_file():
        _log.warning(f"File {grapher.paths.macrostate_file_name} does not exist, will re-take the measurements by"
                     f" re-running the VDF")
        re_measure = True
    if re_measure is False:
        data_means = pd.read_csv(str(grapher.paths.macrostate_file_name))
        plot = grapher.plot_data(
            data=data_means,
            title=title,
            fname=grapher.paths.plot_file_name,
        )

    else:
        result = grapher.collect_pietrzak_complexity_data(fix_input=fix_input, _verbose=verbose,
                                                          store_measurements=store_measurements)

        plot = grapher.plot_data(
            data=result.means,
            title=title,
            fname=grapher.paths.plot_file_name
        )
    print(f"the operation took {t() - s} seconds or {strftime('%H:%M:%S', gmtime(t() - s))}")
    if show:
        plot.show()