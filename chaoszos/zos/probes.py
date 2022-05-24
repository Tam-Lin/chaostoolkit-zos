from chaoslib.types import Configuration, Secrets

from logzero import logger

from chaoslib.exceptions import ActivityFailed, InterruptExecution

from chaoszos.__send_zos_command import Send_Command

__all__ = ["is_responding"]

def is_responding(configuration: Configuration = None, secrets: Secrets = None, location: str = None):
    """
    Checks to make sure that a system is responsive

    :param configuration:
    :param secrets:
    :param location: The z/OS system you want to check for responsiveness
    :return:
    """

    if location is None or location is "":
        raise InterruptExecution("No target specified for action")


    logger.debug(location)

    try:
        d_r_r = Send_Command(location, secrets[location], "D R,R", "IEE112I")
    except KeyError:
        raise InterruptExecution(location + " not found in secrets")
    except TypeError:
        raise InterruptExecution("No secrets specified")
