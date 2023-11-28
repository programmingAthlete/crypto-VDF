import typer

from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)


@app.command(name="pietraz")
def cmd_vdf1():
    pp = PietrzakVDF.setup(security_param=100, delay=8)
    x = PietrzakVDF.gen(pp)
    y = PietrzakVDF.eval_function(public_params=pp, input_param=x)
    print("Output of Eval:", y)
