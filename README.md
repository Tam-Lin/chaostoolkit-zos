# chaostoolkit-zos

[z/OS][zos] support for the [Chaos Toolkit][chaostoolkit].

[zos]: https://www.ibm.com/it-infrastructure/z/zos
[chaostoolkit]: http://chaostoolkit.org/

## Install

This is a plugin for the Chaos Toolkit, so will need to be installed in an environment where that is already installed.  In addition, in order to communicate with z/OS, you will need to use either the z/OSMF Console Services REST interface, the [z/OS Open Automation Utility][zoau] will need to be installed on the z/OS image you will be connecting to, or you will need to be able to connect to the HMC/SE to use the HMC console interfaces.

[zoau]: https://www.ibm.com/support/knowledgecenter/en/SSKFYE_1.0.1/program_directory_zoautil/hal5100.html

## Usage

The current focus is more on actions than probes, as the assumption is that z/OS is part of a system, and you would be using Chaos Toolkit probes from other packages, or the basic http support, to be validating your environment is still working.

## Configuration

### z/OSMF Connection

### zoau Connection

### HMC Connection

## Contribute

## Develop

## Test