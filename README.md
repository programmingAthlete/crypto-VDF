# crypto-VDF

## Advice
Use a virtual python env to avoid installing libraries to your main python version.

## Setup
<code>make deps</code>

### If in addition you want to use the Typer CLI

<code>pip install -e .</code>


## How to run the VFDs 
### with CLI
To run the Eval function of Pietraz, run

<code>cryptoVDF run pietraz</code>

### Without CLI

<code>python src/crypto_VDF/verifiable_delay_functions/pietrzak.py</code>
## Get help
<code>cryptoVDF --help</code>