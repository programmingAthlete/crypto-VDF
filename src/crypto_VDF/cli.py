import typer

from crypto_VDF.verifiable_delay_functions.cli import app as vdf

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)
app.add_typer(vdf, name="run")
