from time import strftime, gmtime
from typing import Annotated

import pandas as pd
import typer
from orjson import orjson

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.data_transfer_objects.plotter import InputType, VDFName
from crypto_VDF.plotter.pietrazk_grapher import PietrzakGrapher
from crypto_VDF.utils.logger import get_logger
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF
from time import time as t

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)

_log = get_logger(__name__)


@app.command(name="full-vdf")
def cmd_full_vdf(
        delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 2,
        security_parameter: Annotated[int, typer.Option(help="Bit lengths of the modulus")] = 10,
        verbose: Annotated[bool, typer.Option(help="Show Debug logs")] = False,
):
    pp = PietrzakVDF.setup(security_param=security_parameter, delay=delay)
    print(f"Public parameters: {orjson.loads(pp.json())}\n")
    x = PietrzakVDF.gen(pp)
    print(f"\nGenerated input: {x}\n")
    evaluation = PietrzakVDF.eval(public_params=pp, input_param=x, _verbose=verbose, _hide=True)
    print(f"\nGenerated output: {evaluation.output}")
    print(f"Generated Proof: {evaluation.proof}\n")
    verif = PietrzakVDF.verify(pp, x, evaluation.output, evaluation.proof, verbose, _hide=True)
    print(f"\nVerification: {verif}")
    assert verif


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


@app.command(name='verify')
def cmd_verif(
        x: Annotated[int, typer.Option(help="Input of eval function")],
        y: Annotated[int, typer.Option(help="Output of eval function")],
        modulus: Annotated[int, typer.Option(help="VDF modulus")],
        proof: Annotated[str, typer.Option(help="Proof outputted by eval")],
        delay: Annotated[int, typer.Option(help="VDF delay")] = 4,
        security_parameter: Annotated[int, typer.Option(help="Security Parameter")] = 128,
        verbose: Annotated[bool, typer.Option(help="Show debug logs")] = False):
    proof = [int(item) for item in proof.split(',')]
    pp = PublicParams(modulus=modulus, delay=delay, security_param=security_parameter)
    out = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=y, proof=proof, _verbose=verbose)
    print(out)


@app.command(name="eval")
def cmd_eval(
        security_parameter: Annotated[int, typer.Option(help="security_parameter")] = 128,
        delay: Annotated[int, typer.Option(help="Delay of the VDF")] = 4
):
    pp = PietrzakVDF.setup(security_param=security_parameter, delay=delay)
    x = PietrzakVDF.gen(pp)
    y = PietrzakVDF.eval(public_params=pp, input_param=x)
    print("Modulus:", pp.modulus)
    print("Output of Eval:", y)


@app.command(name="setup")
def cmd_setup(security_parameter: int = 100, delay: int = 2 ** 10):
    pp = PietrzakVDF.setup(security_param=security_parameter, delay=delay)
    print(f"{orjson.loads(pp.json())}")


@app.command(name="gen")
def cmd_gen(delay: int = 2 ** 10, modulus: int = 21):
    pp = PublicParams(delay=delay, modulus=modulus)
    x = PietrzakVDF.gen(pp)
    print(f"Generated quadratic residue: {x}")


@app.command(name="plots")
def cmd_complexity_plots(
        security_parameter: Annotated[int, typer.Option(help="Security parameter")] = 128,
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
    grapher = PietrzakGrapher(number_of_delays=max_delay_exp, number_ot_iterations=iterations, input_type=input_type,
                              security_parameter=security_parameter)
    title = rf"Pietrzak VDF complexity (mean after {grapher.number_ot_iterations} iterations) $\lambda$ = " \
            rf"{security_parameter}"
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
            vdf_name=VDFName.PIETRZAK
        )

    else:
        result = grapher.collect_pietrzak_complexity_data(fix_input=fix_input, _verbose=verbose,
                                                          store_measurements=store_measurements)

        plot = grapher.plot_data(
            data=result.means,
            title=title,
            fname=grapher.paths.plot_file_name,
            vdf_name=VDFName.PIETRZAK
        )
    print(f"the operation took {t() - s} seconds or {strftime('%H:%M:%S', gmtime(t() - s))}")
    if show:
        plot.show()
