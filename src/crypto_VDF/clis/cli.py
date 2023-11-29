import typer

from crypto_VDF.clis.pietrzak import app as pietrzak
from crypto_VDF.clis.wesolowski import app as wesolowski

app = typer.Typer(pretty_exceptions_show_locals=False, no_args_is_help=True)
app.add_typer(pietrzak, name='pietrzak')
app.add_typer(wesolowski, name='wesolowski')
