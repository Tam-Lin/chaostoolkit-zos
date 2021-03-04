 # Chaos Toolkit Extension for z/OS

[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-zos.svg)](https://www.python.org/)


[z/OS][zos] support for the [Chaos Toolkit][chaostoolkit].

[zos]: https://www.ibm.com/it-infrastructure/z/zos
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-zos
```

In addition, in order to communicate with z/OS, you will need to use either the z/OSMF Console Services REST interface, the [z/OS Open Automation Utility][zoau] will need to be installed on the z/OS image you will be connecting to, or you will need to be able to connect to the HMC/SE to use the HMC console interfaces.

[zoau]: https://www.ibm.com/support/knowledgecenter/en/SSKFYE_1.0.1/program_directory_zoautil/hal5100.html

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json


```

That's it!

Please explore the code to see existing probes and actions.

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe


## Configuration


## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ pip install -e .
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
