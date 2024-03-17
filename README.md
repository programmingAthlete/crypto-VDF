# crypto-VDF
Implementation of two time-lock based-Verifiable Delay Functions.
The two VDFs are
<ul>
  <li>Pietrzark's VDF: https://eprint.iacr.org/2018/627.pdf</li>
  <li>Wesoloski's VDF: https://eprint.iacr.org/2018/623</li>
</ul>
In the case Wesoloski's VDF, our disign implementation of the optimization of the proof, slightly diverged from the original one. Our solution is more efficient compared to the paper's one when restricting to binary values b_is (binar repreentation of the proof - kappa = 1), but it is not more efficinet in general.

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
<li>requirements-tests.txt - dependencies file for the tests (dependencies for the project + potential additional dependencies)</li>
<li>setup.py - installation file for the package</li>
<li>setup.cfg - file containing additional information for the setup of the project (such as the CLI entry point) and potential settings for linting and test coverage</li>
</ul>

## Setup
Install the package using

<code>make setup</code>


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

## Examples

### Compute and Verify

Delay of 2^(10)

<code>cryptoVDF pietrzak generate-and-verify 359 --delay 1024 --modulus 437 --verbose</code>

Delay of 2^(20)

<code>cryptoVDF pietrzak generate-and-verify 359 --delay 1048576 --modulus 437 --verbose</code>

# Full VDF
Delay of 2^(20)

<code>cryptoVDF pietrzak full-vdf --delay 1048576 --security-parameter 128</code>

<code>cryptoVDF wesolowski full-vdf --delay 1048576 --security-parameter 128</code>

<code>cryptoVDF wesolowski full-vdf --delay 1048576 --security-parameter 128 --trapdoor</code>

# Plots
<code>cryptoVDF wesolowski plots --max-delay-exp 10 --iterations 20  --show</code>

<code>cryptoVDF pietrzak plots --max-delay-exp 10 --iterations 20  --show</code>

<code>cryptoVDF pietrzak plots --max-delay-exp 8 --iterations 2 --security-parameter 4 --show --verbose</code>

<code>cryptoVDF pietrzak plots --max-delay-exp 10 --iterations 400 --security-parameter 4 --show --verbose</code>

<code>cryptoVDF pietrzak plots --max-delay-exp 10 --iterations 10 --security-parameter 128 --show --verbose</code>

<code>cryptoVDF wesolowski plots --max-delay-exp 10 --iterations 10 --security-parameter 128 --show --verbose</code>

<code>cryptoVDF pietrzak plots --max-delay-exp 10 --iterations 10 --security-parameter 128 --show --verbose</code>


# Demo

## Full-VDF

### Completeness
<code>cryptoVDF pietrzak full-vdf --delay 1048576 --security-parameter 128</code>

<code>cryptoVDF wesolowski full-vdf --delay 1048576 --security-parameter 128</code>

<code>cryptoVDF wesolowski full-vdf --delay 1048576 --security-parameter 128 --trapdoor</code>

### Soundness
### VDF1

<code>cryptoVDF pietrzak eval --security-parameter 128 --delay 4</code>

<code>cryptoVDF pietrzak verify --x input --y output --proof proof --modulus modulus --security-parameter security-parameter</code>

Example: The following should evaluate to True

<code>cryptoVDF pietrzak verify --x 60165111687309026253618363786070190189 --y 38920676524930194932948449234450122897 --proof 26733557083776090708288610604071675446,54679161191322144951368137116431681903 --modulus 202791651255554990394641179601075112913 --security-parameter 128</code>

#### VDF2
<code>cryptoVDF wesolowski eval --security-parameter 128 --delay 4</code>

<code>cryptoVDF wesolowski verify --x input --y output --proof proof --delay delay --modulus modulus</code>

Example: The following will return True

<code>cryptoVDF wesolowski verify --x 95974600194182310684653862122690543205 --y 856966856996350542601758883331119 --proof 95974600194182310684653862122690543205 --delay 4 --modulus 100167473050021300389050029515619897043<code>




## Plots
<code>cryptoVDF pietrzak plots --max-delay-exp 10 --iterations 200 --security-parameter 4 --show</code>

<code>cryptoVDF wesolowski plots --max-delay-exp 10 --iterations 200 --security-parameter 4 --show</code>

