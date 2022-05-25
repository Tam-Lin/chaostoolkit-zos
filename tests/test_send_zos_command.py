from unittest.mock import patch
from chaoslib.exceptions import InterruptExecution
from chaoszos.__send_zos_command import Send_Command, EmptyCommand

import pytest

import zhmcclient


def test_send_empty_command():

    connection_information = {'method': 'hmc',
                              'hostname': 'fake_hostname',
                              'userid': 'fake_userid',
                              'password': 'fake_password'}

    location = "M89 S5C"

    with pytest.raises(EmptyCommand):
        Send_Command(location, connection_information, None, None)


@patch('zhmcclient.Session')
def test_send_command_using_zhmcclient_unable_to_connect(mock_session):
    mock_session.side_effect = zhmcclient.ConnectionError("", "")

    connection_information = {'method': 'hmc',
                              'hostname': 'fake_hostname',
                              'userid': 'fake_userid',
                              'password': 'fake_password'}

    location = "M89 S5C"

    with pytest.raises(InterruptExecution):

        Send_Command(location, connection_information, 'D R,R', 'IEE112I')
