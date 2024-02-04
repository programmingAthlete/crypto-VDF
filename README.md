# crypto-VDF

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

## Rules
<ul>
<li>
Merging to the master branch should be done only by PR unless proper justification or it the changes to not impact critical structure (for example CLI changes which have nothing to do with the crypto part)
</li>
<li>
When merging to master the feature branch should be up-to-date - best thing to do would be to rebase the feature branch into master: <b>in the feature branch</b> do
<code>git rebase develop</code>, then <code>git push -f</code>
</li>
<li>A feature branch should be merged only if its unit tests pass</li>
<li>The merge to master branch should be done from the GitHub UI using the <b>squash and merge</b> option if the branch contains more than one commit</li>
</ul>

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

### Completemess
<code>cryptoVDF pietrzak full-vdf --delay 1048576 --security-parameter 128</code>

<code>cryptoVDF wesolowski full-vdf --delay 1048576 --security-parameter 128</code>

<code>cryptoVDF wesolowski full-vdf --delay 1048576 --security-parameter 128 --trapdoor</code>

### Soundness
### VDF1

<code>cryptoVDF pietrzak eval --security-parameter 128 --delay 4</code>

<code>cryptoVDF pietrzak verify --x input --y output --proof proof --modulus modulus --security-parameter security-parameter</code>

#### VDF2
<code>cryptoVDF wesolowski eval --security-parameter 128 --delay 4</code>

<code>cryptoVDF wesolowski verify --x input --y output --proof proof --delay delay --modulus modulus</code>

Example: Teh following will return True
<code>cryptoVDF wesolowski verify --x 95974600194182310684653862122690543205 --y 856966856996350542601758883331119 --proof 95974600194182310684653862122690543205 --delay 4 --modulus 100167473050021300389050029515619897043<code>




## Plots
<code>cryptoVDF pietrzak plots --max-delay-exp 10 --iterations 200 --security-parameter 4 --show</code>

<code>cryptoVDF wesolowski plots --max-delay-exp 10 --iterations 200 --security-parameter 4 --show</code>

