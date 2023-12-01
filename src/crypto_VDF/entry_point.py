from crypto_VDF.clis import cli


def main():
    cli.app(prog_name='cryptoVDF')
    cli.app.add_typer()
