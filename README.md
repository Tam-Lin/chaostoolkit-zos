# [Chaos Toolkit Extension for z/OS]()

This project is a collection of [actions][] and [probes][] to allow the [Chaos Toolkit][chaostoolkit] to interact
with [z/OS].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action

[probes]: http://chaostoolkit.org/reference/api/experiment/#probe

[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

This package needs to be installed in a Python environment where the [chaostoolkit][] is already installed.

``pip install -U chaostoolkit-zos``

## Usage

To use the actions in the package, add the following to your experiment file:

```json
{
  "name": "configure_all_ziips_offline",
  "provider": {
    "type": "python",
    "module": "chaoszos.zos.actions",
    "func": "configure_processors",
    "secrets": [
      "zos_console"
    ],
    "arguments": {
      "location": "S5C",
      "processor_type": "ziip",
      "status": "offline"
    }
  }
}
```

## Configuration

### Access Methods

There are a number of different ways to interact with z/OS, and a number of interfaces for each method of interaction.
For example, to issue a z/OS console command, you can connect to an HMC/SE, use the ZOAU interfaces, Ansible, the z/OSMF
REST APIs, or Zowe. Similarly, for submitting jobs, you can use FTP, or zoau, or Zowe, or z/OSMF. And different
installations have different legal and security requirements that will dictate which methods could be used. As such, the
toolkit plans to allow multiple ways of doing any of these activities, without needing to change your high level
experiment. The contents of your secrets will dictate which access method is used for a given experiment.

### Credentials

In order to issue commands, you need to give the extension a couple of pieces of information:  how to connect to z/OS or
the subsystem, and credentials to connect. In order to make this as transparent as possible, you can specify this
information in your secrets section, and not have to change the experiment itself at all. For example, to use the z/OS
hmc to issue commands in the above sample, you could specify

```json
{
  "secrets": {
    "zos_console": {
      "S5C": {
        "method": "hmc",
        "hostname": "ioshmc3.pok.stglabs.ibm.com",
        "userid": {
          "type": "env",
          "key": "IOSHMC3_USERID"
        },
        "password": {
          "type": "env",
          "key": "IOSHMC3_PASSWORD"
        }
      }
    }
  }
}
```

Or, to use the Ansible interface, provided by ZOAU, you could specify

```json
{
  "secrets": {
    "zos_console": {
      "S5C": {
        "method": "ansible",
        "hostname": "pksts5c.pok.stglabs.ibm.com",
        "userid": {
          "type": "env",
          "key": "S5C_USERID"
        },
        "password": {
          "type": "env",
          "key": "S5C_PASSWORD"
        }
      }
    }
  }
}
```

## Contribute

If you wish to contribute more functions to this package, you are welcome to do so. First, fork this project,
make your changes following the usual [PEP 8][pep8] code style, add tests and submit a PR for review.  Or, if you'd like to be able to do somehting with the Chaos Toolkit, but don't know how to do it via code, feel free to submit a problem report, and I'll see what I can figure out.  I'm hoping to add support for z/OS subsystems (CICS, Db2, IMS, etc), but my exptertise is in z/OS, so I need to understand what sorts of things you'd like to be able to do.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge into the master branch of the repository.
Please, make sure you can abide by the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development dependencies. But
first, [create a virtual environment][venv] and then install those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your environment, even when running from
the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
