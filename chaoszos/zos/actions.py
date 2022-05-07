# -*- coding: utf-8 -*-
from typing import Dict, List, Any, AnyStr

from chaoslib.exceptions import ActivityFailed, InterruptExecution
from chaoslib.types import Configuration, Secrets

from logzero import logger

from zos_utilities.lpar import LPAR, LPARException

from chaoszos.__send_zos_command import Send_Command

__all__ = ["configure_processors"]

def configure_processors(configuration: Configuration = None, secrets: Secrets = None,
                         processor_type_to_change: str = None,
                         processor_count_to_change: int = None, status_to_change_to: str = None, location: str = None):

    """
    Configures processors either offline or online, depending on the action

    If neither processor count or processor list is specified, the assumption is you want to configure
    all processors of a given type offline or online.  This is only valid for zIIPs.

    :param configuration:
    :param secrets:
    :param processor_type_to_change: Type of processors to configure offline.  Can be None, cp, or ziip
    :param processor_count_to_change:  The number of processors to configure; if None, defaults to all processors of that type
    :param status_to_change_to:  Intended final configuration (offline or online)
    :param location:  The z/OS image you want to configure processors
    :return:
    """

    logger.debug("Configuration: %s" % configuration)
    logger.debug("processor_type_to_change: %s" % processor_type_to_change)
    logger.debug("processor_count_to_change: %s" % processor_count_to_change)
    logger.debug("status: %s" % status_to_change_to)
    logger.debug("location: %s" % location)

    if processor_type_to_change is not None and processor_type_to_change != "ziip" and processor_type_to_change != "cp":
        raise InterruptExecution("Invalid processor type specified")

    if status_to_change_to != "online" and status_to_change_to != "offline":
        raise InterruptExecution("status_to_change_to must be online or offline; got %s" % status_to_change_to)

    if processor_count_to_change is None and (processor_type_to_change is None or processor_type_to_change == "cp") and status_to_change_to == "offline":
        raise InterruptExecution("Can not configure all CPs offline")

    if location is None or location is "":
        raise InterruptExecution("No target specified for action")

    try:
        dmcore = Send_Command(location, secrets[location], "D M=CORE", "IEE174I")
    except KeyError:
        raise InterruptExecution(location + " not found in secrets")
    except TypeError:
        raise InterruptExecution("No secrets specified")

    test_lpar = LPAR()

    test_lpar.parse_d_m_core(dmcore.message_out)

    processors_remaining_to_change = processor_count_to_change

    logger.debug("Changing %s prcoessors of type %s to %s" % (processors_remaining_to_change, processor_type_to_change, status_to_change_to))

    for (processor_name, processor) in test_lpar.logical_processors.items():

        logger.debug(processor)

        if (processor_type_to_change == "ziip" and processor.type == "zIIP") or (processor_type_to_change == "cp" and processor.type == "CP"):
            if (status_to_change_to == "offline" and processor.online == True) or (status_to_change_to == "online" and processor.online == False):
                logger.info("Configuring CORE " + processor.coreid + " " + status_to_change_to.upper())
                configure_command = Send_Command(location, secrets[location], "CF CORE(" + processor.coreid + ")," + status_to_change_to.upper(), "IEE505I")

                if processors_remaining_to_change is not None:
                    processors_remaining_to_change = processors_remaining_to_change - 1

                    logger.debug("%s processors left to change" % (processors_remaining_to_change))

        if processors_remaining_to_change is 0:
            break