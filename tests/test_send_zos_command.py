from unittest.mock import patch, MagicMock
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


@patch('paramiko.SSHClient')
def test_send_command_using_ssh_command_succeeds_v1_1_1(mock_paramiko_client):
    location = "fake_hostname"
    connection_information = {'method': 'ssh',
                              'hostname': 'fake_hostname',
                              'userid': 'fake_userid',
                              'password': 'fake_password'}

    stdin = [""]
    stderr = [""]

    stdout = [
        'CB8A      202216   12:41:20.49             ISF041I CONSOLE NAME MCKENZI MODIFIED TO MCKENZI$',
        'CB8A      202216   12:41:20.49             ISF031I CONSOLE MCKENZI$ ACTIVATED',
        'CB8A      202216   12:41:20.49            -D M=CORE',
        'CB8A      202216   12:41:20.51             IEE174I 12.41.20 DISPLAY M 813',
        '                                           CORE STATUS: HD=Y   MT=2  MT_MODE: CP=1  zIIP=2',
        '                                           ID    ST   ID RANGE   VP  ISCM  CPU THREAD STATUS',
        '                                           0000   +   0000-0001  H   FC00  +N',
        '                                           0001   +   0002-0003  M   0000  +N',
        '                                           0002   +   0004-0005  L   0000  +N',
        '                                           0003   +   0006-0007  L   0000  +N',
        '                                           0004   +   0008-0009  LP  0000  +N',
        '                                           0005   +   000A-000B  LP  0000  +N',
        '                                           0006   +   000C-000D  LP  0000  +N',
        '                                           0007   +   000E-000F  LP  0000  +N',
        '                                           0008   +   0010-0011  LP  0000  +N',
        '                                           0009   +   0012-0013  LP  0000  +N',
        '                                           000A   +   0014-0015  LP  0000  +N',
        '                                           000B   +   0016-0017  LP  0000  +N',
        '                                           000C   +   0018-0019  LP  0000  +N',
        '                                           000D   +   001A-001B  LP  0000  +N',
        '                                           000E   +   001C-001D  LP  0000  +N',
        '                                           000F   +   001E-001F  LP  0000  +N',
        '                                           0010   +   0020-0021  LP  0000  +N',
        '                                           0011   +   0022-0023  LP  0000  +N',
        '                                           0012   +   0024-0025  LP  0000  +N',
        '                                           0013   +   0026-0027  LP  0000  +N',
        '                                           0014   +I  0028-0029  M   0200  ++',
        '                                           0015   -I  002A-002B',
        '                                           0016   -I  002C-002D',
        '                                           0017   -I  002E-002F',
        '                                           0018   +I  0030-0031  M   0200  ++',
        '                                           0019   +I  0032-0033  LP  0200  ++',
        '                                           001A   +I  0034-0035  LP  0200  ++',
        '                                           001B   +I  0036-0037  LP  0200  ++',
        '                                           001C   +I  0038-0039  LP  0200  ++',
        '                                           001D   +I  003A-003B  LP  0200  ++',
        '                                           001E   +I  003C-003D  LP  0200  ++',
        '                                           001F   +I  003E-003F  LP  0200  ++',
        '                                           0020   +I  0040-0041  LP  0200  ++',
        '                                           0021   +I  0042-0043  LP  0200  ++',
        '                                           0022   +I  0044-0045  LP  0200  ++',
        '                                           0023   +I  0046-0047  LP  0200  ++',
        '                                           0024   NI  0048-0049',
        '                                           0025   NI  004A-004B',
        '                                           0026   NI  004C-004D',
        '                                           0027   NI  004E-004F',
        '                                           0028   NI  0050-0051',
        '                                           0029   NI  0052-0053',
        '                                           002A   NI  0054-0055',
        '                                           002B   NI  0056-0057', '',
        '                                           CPC ND = 008561.T01.IBM.02.000000000078',
        '                                           CPC SI = 8561.775.IBM.02.0000000000000078',
        '                                                    Model: T01',
        '                                           CPC ID = 00',
        '                                           CPC NAME = T78',
        '                                           LP NAME = CB8A       LP ID = 1B',
        '                                           CSS ID  = 1',
        '                                           MIF ID  = B', '',
        '                                           + ONLINE    - OFFLINE    N NOT AVAILABLE    / MIXED STATE',
        '                                           W WLM-MANAGED', '',
        '                                           I        INTEGRATED INFORMATION PROCESSOR (zIIP)',
        '                                           CPC ND  CENTRAL PROCESSING COMPLEX NODE DESCRIPTOR',
        '                                           CPC SI  SYSTEM INFORMATION FROM STSI INSTRUCTION',
        '                                           CPC ID  CENTRAL PROCESSING COMPLEX IDENTIFIER',
        '                                           CPC NAME CENTRAL PROCESSING COMPLEX NAME',
        '                                           LP NAME  LOGICAL PARTITION NAME',
        '                                           LP ID    LOGICAL PARTITION IDENTIFIER',
        '                                           CSS ID   CHANNEL SUBSYSTEM IDENTIFIER',
        '                                           MIF ID   MULTIPLE IMAGE FACILITY IMAGE IDENTIFIER']

    mock_paramiko_client.return_value.exec_command.return_value = (stdin, stdout, stderr)

    command_output = Send_Command(location, connection_information, 'D M=CORE', 'IEE174I')

    assert command_output.message_out[0] == 'IEE174I 12.41.20 DISPLAY M 813'
    assert command_output.message_out[-1] == 'MIF ID   MULTIPLE IMAGE FACILITY IMAGE IDENTIFIER'


@patch('paramiko.SSHClient')
def test_send_command_using_ssh_command_succeeds_v1_1_1_b(mock_paramiko_client):
    location = "fake_hostname"
    connection_information = {'method': 'ssh',
                              'hostname': 'fake_hostname',
                              'userid': 'fake_userid',
                              'password': 'fake_password'}

    stdin = [""]
    stderr = [""]

    stdout = ['CB8A      202216   16:27:20.64             ISF031I CONSOLE MCKENZI ACTIVATED',
              'CB8A      202216   16:27:20.64            -D M=CORE',
              'CB8A      202216   16:27:20.66             IEE174I 16.27.20 DISPLAY M 677',
              '                                           CORE STATUS: HD=Y   MT=2  MT_MODE: CP=1  zIIP=2',
              '                                           ID    ST   ID RANGE   VP  ISCM  CPU THREAD STATUS',
              '                                           0000   +   0000-0001  H   FC00  +N',
              '                                           0001   +   0002-0003  M   0000  +N',
              '                                           0002   +   0004-0005  L   0000  +N',
              '                                           0003   +   0006-0007  L   0000  +N',
              '                                           0004   +   0008-0009  LP  0000  +N',
              '                                           0005   +   000A-000B  LP  0000  +N',
              '                                           0006   +   000C-000D  LP  0000  +N',
              '                                           0007   +   000E-000F  LP  0000  +N',
              '                                           0008   +   0010-0011  LP  0000  +N',
              '                                           0009   +   0012-0013  LP  0000  +N',
              '                                           000A   +   0014-0015  LP  0000  +N',
              '                                           000B   +   0016-0017  LP  0000  +N',
              '                                           000C   +   0018-0019  LP  0000  +N',
              '                                           000D   +   001A-001B  LP  0000  +N',
              '                                           000E   +   001C-001D  LP  0000  +N',
              '                                           000F   +   001E-001F  LP  0000  +N',
              '                                           0010   +   0020-0021  LP  0000  +N',
              '                                           0011   +   0022-0023  LP  0000  +N',
              '                                           0012   +   0024-0025  LP  0000  +N',
              '                                           0013   +   0026-0027  LP  0000  +N',
              '                                           0014   +I  0028-0029  M   0200  ++',
              '                                           0015   -I  002A-002B',
              '                                           0016   -I  002C-002D',
              '                                           0017   -I  002E-002F',
              '                                           0018   +I  0030-0031  M   0200  ++',
              '                                           0019   +I  0032-0033  LP  0200  ++',
              '                                           001A   +I  0034-0035  LP  0200  ++',
              '                                           001B   +I  0036-0037  LP  0200  ++',
              '                                           001C   +I  0038-0039  LP  0200  ++',
              '                                           001D   +I  003A-003B  LP  0200  ++',
              '                                           001E   +I  003C-003D  LP  0200  ++',
              '                                           001F   +I  003E-003F  LP  0200  ++',
              '                                           0020   +I  0040-0041  LP  0200  ++',
              '                                           0021   +I  0042-0043  LP  0200  ++',
              '                                           0022   +I  0044-0045  LP  0200  ++',
              '                                           0023   +I  0046-0047  LP  0200  ++',
              '                                           0024   NI  0048-0049',
              '                                           0025   NI  004A-004B',
              '                                           0026   NI  004C-004D',
              '                                           0027   NI  004E-004F',
              '                                           0028   NI  0050-0051',
              '                                           0029   NI  0052-0053',
              '                                           002A   NI  0054-0055',
              '                                           002B   NI  0056-0057', '',
              '                                           CPC ND = 008561.T01.IBM.02.000000000078',
              '                                           CPC SI = 8561.775.IBM.02.0000000000000078',
              '                                                    Model: T01',
              '                                           CPC ID = 00',
              '                                           CPC NAME = T78',
              '                                           LP NAME = CB8A       LP ID = 1B',
              '                                           CSS ID  = 1',
              '                                           MIF ID  = B', '',
              '                                           + ONLINE    - OFFLINE    N NOT AVAILABLE    / MIXED STATE',
              '                                           W WLM-MANAGED', '',
              '                                           I        INTEGRATED INFORMATION PROCESSOR (zIIP)',
              '                                           CPC ND  CENTRAL PROCESSING COMPLEX NODE DESCRIPTOR',
              '                                           CPC SI  SYSTEM INFORMATION FROM STSI INSTRUCTION',
              '                                           CPC ID  CENTRAL PROCESSING COMPLEX IDENTIFIER',
              '                                           CPC NAME CENTRAL PROCESSING COMPLEX NAME',
              '                                           LP NAME  LOGICAL PARTITION NAME',
              '                                           LP ID    LOGICAL PARTITION IDENTIFIER',
              '                                           CSS ID   CHANNEL SUBSYSTEM IDENTIFIER',
              '                                           MIF ID   MULTIPLE IMAGE FACILITY IMAGE IDENTIFIER']

    mock_paramiko_client.return_value.exec_command.return_value = (stdin, stdout, stderr)

    command_output = Send_Command(location, connection_information, 'D M=CORE', 'IEE174I')

    assert command_output.message_out[0] == 'IEE174I 16.27.20 DISPLAY M 677'
    assert command_output.message_out[-1] == 'MIF ID   MULTIPLE IMAGE FACILITY IMAGE IDENTIFIER'


@patch('paramiko.SSHClient')
def test_send_command_using_ssh_command_succeeds_v1_2_0(mock_paramiko_client):
    location = "fake_hostname"
    connection_information = {'method': 'ssh',
                              'hostname': 'fake_hostname',
                              'userid': 'fake_userid',
                              'password': 'fake_password'}

    stdin = [""]
    stderr = [""]

    stdout = [
        '        C0A       2024164  15:15:13.39             ISF031I CONSOLE MYCONS ACTIVATED',
        'C0A       2024164  15:15:13.39            -d r,r',
        'C0A       2024164  15:15:13.40             IEE112I 15.15.13 PENDING REQUESTS 249',
        '                                           RM=21   IM=0     CEM=0     EM=0     RU=0    IR=0    AMRF',
        '                                           ID:R/K     T SYSNAME  MESSAGE TEXT'
    ]

    mock_paramiko_client.return_value.exec_command.return_value = (stdin, stdout, stderr)

    command_output = Send_Command(location, connection_information, 'D R,R', 'IEE112I')

    assert command_output.message_out[0] == 'IEE112I 15.15.13 PENDING REQUESTS 249'
    assert command_output.message_out[-1] == "ID:R/K     T SYSNAME  MESSAGE TEXT"
