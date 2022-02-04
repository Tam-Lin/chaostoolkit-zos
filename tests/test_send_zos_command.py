from unittest.mock import patch
from chaoslib.exceptions import InterruptExecution
from chaoszos.__send_zos_command import Send_Command, EmptyCommand

import pytest

import zhmcclient_mock
import zhmcclient


def test_send_empty_command():

    connection_information = {'method': 'hmc', 'hostname': 'fake_hostname', 'userid': 'fake_userid',
                              'password': 'fake_password'}

    location = "M89 S5C"

    with pytest.raises(EmptyCommand):
        command = Send_Command(location, connection_information, None, None)

@patch('zhmcclient.Session')
def test_send_command_using_zhmcclient_unable_to_connect(mock_session):
    mock_session.side_effect = zhmcclient.ConnectionError("", "")

    connection_information = {'method': 'hmc', 'hostname': 'fake_hostname', 'userid': 'fake_userid',
                              'password': 'fake_password'}

    location = "M89 S5C"

    with pytest.raises(InterruptExecution):
        command = Send_Command(location, connection_information, 'D R,R', 'IEE112I')


def test_send_command_using_zhmcclient():

    connection_information = {'method': 'hmc', 'hostname': 'fake_hostname', 'userid': 'fake_userid',
                              'password': 'fake_password'}

    location = "M89 S5C"

    with patch('zhmcclient.Session', new=zhmcclient_mock.FakedSession('fake_hostname', 'fake_userid', '2.13.1', '1.8')) as fake_session:
        command = Send_Command(location, connection_information, 'D M=CORE', 'IEE174I')

        assert command.message_out == [
'IEE174I 16.54.16 DISPLAY M 923                   ',
'CORE STATUS: HD=Y   MT=2  MT_MODE: CP=1  zIIP=1  ',
'ID    ST   ID RANGE   VP  ISCM  CPU THREAD STATUS',
'0000   +   0000-0001  H   FC00  +N               ',
'0001   +   0002-0003  H   0000  +N               ',
'0002   +   0004-0005  H   0000  +N               ',
'0003   +   0006-0007  H   0000  +N               ',
'0004   +   0008-0009  H   0000  +N               ',
'0005   +   000A-000B  H   0000  +N               ',
'0006   +   000C-000D  H   0000  +N               ',
'0007   +   000E-000F  H   0000  +N               ',
'0008   +   0010-0011  H   0000  +N               ',
'0009   +   0012-0013  H   0000  +N               ',
'000A   +   0014-0015  H   0000  +N               ',
'000B   +   0016-0017  H   0000  +N               ',
'000C   +   0018-0019  H   0000  +N               ',
'000D   +   001A-001B  H   0000  +N               ',
'000E   +   001C-001D  H   0000  +N               ',
'000F   +   001E-001F  H   0000  +N               ',
        ]


def test_send_command_using_ssh():

    connection_information = {'method': 'ssh', 'hostname': 'fake_hostname', 'userid': 'fake_userid',
                              'password': 'fake_password'}

    command = Send_Command(location, connection_information, 'D M=CORE', 'IEE174I')

    assert command.message_out == [
        'IEE174I 16.54.16 DISPLAY M 923                   ',
        'CORE STATUS: HD=Y   MT=2  MT_MODE: CP=1  zIIP=1  ',
        'ID    ST   ID RANGE   VP  ISCM  CPU THREAD STATUS',
        '0000   +   0000-0001  H   FC00  +N               ',
        '0001   +   0002-0003  H   0000  +N               ',
        '0002   +   0004-0005  H   0000  +N               ',
        '0003   +   0006-0007  H   0000  +N               ',
        '0004   +   0008-0009  H   0000  +N               ',
        '0005   +   000A-000B  H   0000  +N               ',
        '0006   +   000C-000D  H   0000  +N               ',
        '0007   +   000E-000F  H   0000  +N               ',
        '0008   +   0010-0011  H   0000  +N               ',
        '0009   +   0012-0013  H   0000  +N               ',
        '000A   +   0014-0015  H   0000  +N               ',
        '000B   +   0016-0017  H   0000  +N               ',
        '000C   +   0018-0019  H   0000  +N               ',
        '000D   +   001A-001B  H   0000  +N               ',
        '000E   +   001C-001D  H   0000  +N               ',
        '000F   +   001E-001F  H   0000  +N               ',
    ]

