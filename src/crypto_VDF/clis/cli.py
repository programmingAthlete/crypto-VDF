import typer

from crypto_VDF.clis.pietrak import app as pietrak
from crypto_VDF.clis.wesolowski import app as wesolowski

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)
app.add_typer(pietrak, name='pietrak')
app.add_typer(wesolowski, name='wesolowski')
