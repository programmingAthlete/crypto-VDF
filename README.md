# crypto-VDF
The source code is organised in a package, inside the 'src' folder.

## Advice
Use a virtual python env to avoid installing libraries to your main python version.

## Organisation of the repo
### Organisation of the package
<ul>
<li>clis - directory to handle the Typer CLI</li>
<li>custom_error - directory containing custom exception classes to facilitate the error handling</li>
<li>data_transfer_objects - directory containing 'contracts' between functions (input and output pydantic models)</li>
<li>utils - directory containing some utilities function such has prime number generators, quadratic residues generators and square-and-multiply function</li>
<li>
verifiable_delay_functions - directory containing the actual VDFs source code
<ul>
<li>vdf.py - file containing the VDF abstract class</li>
<li>pietrzak.py - file containing the Pietrzak VDF (VDF1)</li>
<li>wesolowski.py - file containing the Wesolowski VDF (VDF2)</li>
</ul>
</li>
<li>entry_point.py - entrypoint file for the Typer CLI</li>
</ul>

### Files outside of the source directory
Ourside of the source folder, the following files can be found
<ul>
<li>Makefile</li>
<li>requirements.txt - dependencies file for the project</li>
<li>requirements.txt - dependencies file for the tests (dependencies for the project + potential additional dependencies)</li>
<li>setup.py - installation file for the package</li>
<li>setup.cfg - file containing additional information for the setup of the project (such as the CLI entry point) and potential settings for linting and test coverage</li>
</ul>

## Setup
Install the dependencies using

<code>make deps</code>

<b>If in addition to use the Typer CLI (optional)</b>

<code>pip install -e .</code>


## How to run the VFDs 
### With CLI
To run the VDFs from the CLI run 

<code>cryptoVDF --help</code>

and see the options.

For example, suppose you want to run the Pietrzak eval function, use

<code>cryptoVDF pietrzak eval</code>

### Without CLI
Without CLI, the source code can be run in a classic manner

<code>python src/crypto_VDF/verifiable_delay_functions/pietrzak.py</code>


## How to run unittests
To run the unit tests, run 

<code>make tests</code>