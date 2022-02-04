# -*- coding: utf-8 -*-
from typing import Dict, List, Any, AnyStr

from chaoslib.exceptions import ActivityFailed, InterruptExecution
from chaoslib.types import Configuration, Secrets

from logzero import logger
import re

from chaoszos.__send_zos_command import Send_Command

__all__ = ["configure_processors"]

def configure_processors(configuration: Configuration = None, secrets: Secrets = None, processor_type: str = None,
                         processor_count: int = None, status: str = None, location: str = None):

    """
    Configures processors either offline or online, depending on the action

    If neither processor count or processor list is specified, the assumption is you want to configure
    all processors of a given type offline or online.  This is only valid for zIIPs.

    :param configuration:
    :param secrets:
    :param processor_type: Type of processors to configure offline.  Can be None, cp, or ziip
    :param processor_count:  The number of processors to configure
    :param status:  Intended final configuration
    :param location:  The image you want to configure processors
    :return:
    """

    if processor_type is not None and processor_type != "ziip" and processor_type != "cp":
        raise InterruptExecution("Invalid processor type specified")

    if status != "online" and status != "offline":
        raise InterruptExecution("Status must be online or offline")

    if processor_count is None and (processor_type is None or processor_type == "cp") and status == "offline":
        raise InterruptExecution("Can not configure all CPs offline")

    if location is None or location is "":
        raise InterruptExecution("No target specified for action")

    try:
        dmcore = Send_Command(location, secrets[location], "D M=CORE", "IEE174I")
    except KeyError:
        raise InterruptExecution(location + " not found in secrets")

    core_re = re.compile(
        "(?P<coreid>[0-9A-F]{4})  (?P<wlmmanaged>.)(?P<online>.)(?P<type>.)  (?P<lowcp>[0-9A-F]{4})-(?P<highcp>[0-9A-F]{4})(  (?P<polarity>.)(?P<parked>.)  (?P<subclassmask>[0-9A-F]{4})  (?P<state1>.)(?P<state2>.))?")

    core_list = list()

    for line in dmcore.message_out[3:]:

        core_info = core_re.search(line)

        if core_info is None:
            break
        else:
            core = dict()
            core["coreid"] = core_info.group("coreid")
            core["type"] = core_info.group("type")
            core["online"] = core_info.group("online")

            core_list.append(core)

    #really can clean you up; need to deal with CORE and CPU variations
    for core in core_list:
        logger.debug(core)

        if (processor_type == "ziip" and core["type"] == "I") or (processor_type == "cp" and core["type"] == "C"):
            if (status == "offline" and core["online"] == "+") or (status == "online" and core["online"] == "-"):
                logger.info("Configuring CORE " + core["coreid"] + status)
                configure_command = Send_Command(location, secrets[location], "CF CORE(" + core["coreid"] + ")," + status, "IEE712I")



