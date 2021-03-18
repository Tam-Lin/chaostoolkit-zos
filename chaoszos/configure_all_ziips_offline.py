#!/usr/bin/env python
# Copyright 2017 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Example that shows how to send a system command.
"""

import sys
import re

from chaoslib.discovery.discover import (discover_actions, discover_probes,
                                         initialize_discovery_result)
from chaoslib.exceptions import DiscoveryFailed, InterruptExecution
from chaoslib.types import (Configuration, DiscoveredActivities,
                            DiscoveredSystemInfo, Discovery, Secrets)

import secrets

from __send_zos_command import Send_Command

dmcore = Send_Command(target, secrets['zos_console'],  "D M=CORE", "IEE174I")

core_re = re.compile("(?P<coreid>[0-9A-F]{4})  (?P<wlmmanaged>.)(?P<online>.)(?P<type>.)  (?P<lowcp>[0-9A-F]{4})-(?P<highcp>[0-9A-F]{4})(  (?P<polarity>.)(?P<parked>.)  (?P<subclassmask>[0-9A-F]{4})  (?P<state1>.)(?P<state2>.))?")

core_list = list()

for line in dmcore.message_out.splitlines()[3:]:

    core_info = core_re.search(line)

    if core_info is None:
        break
    else:
        core = dict()
        core["coreid"] = core_info.group("coreid")
        core["type"] = core_info.group("type")
        core["online"] = core_info.group("online")

        core_list.append(core)

for core in core_list:
    print(core)

    if (core["type"] == "I" and core["online"] == "+"):

            print("Configuring CORE " + core["coreid"] + " Offline")
            cfoffline = Send_Command(hmccreds_location, "CF CORE(" + core["coreid"] + "),OFFLINE", None)

dmcore = Send_Command(hmccreds_location, "D M=CORE", "IEE174I")

core_list = list()

for line in dmcore.message_out.splitlines()[3:]:

    core_info = core_re.search(line)

    if core_info is None:
        break
    else:
        core = dict()
        core["coreid"] = core_info.group("coreid")
        core["type"] = core_info.group("type")
        core["online"] = core_info.group("online")

        core_list.append(core)

for core in core_list:
    print(core)

    if (core["type"] == "I" and core["online"] == "-"):

            print("Configuring CORE " + core["coreid"] + " ONLINE")
            cfoffline = Send_Command(hmccreds_location, "CF CORE(" + core["coreid"] + "),ONLINE", None)
