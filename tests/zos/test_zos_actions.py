from unittest.mock import MagicMock, patch

import chaoszos.zos.actions
from chaoslib.exceptions import InterruptExecution

import pytest


@patch('chaoszos.zos.actions.Send_Command', autospec=True)
def test_configure_all_ziip_cores_offline(send_command):
    secrets = dict()
    secrets["SYS1"] = "password1"

    send_command_1 = MagicMock()
    send_command_2 = MagicMock()
    send_command_3 = MagicMock()
    send_command_4 = MagicMock()
    send_command_5 = MagicMock()

    send_command_1.message_out = [
        'IEE174I 14.12.45 DISPLAY M 781                   ',
        'CORE STATUS: HD=Y   MT=1                         ',
        'ID    ST   ID RANGE   VP  ISCM  CPU THREAD STATUS',
        '0000   +   0000-0000  H   FC00  +                ',
        '0001   +   0001-0001  M   0000  +                ',
        '0002   +   0002-0002  LP  0000  +                ',
        '0003   +   0003-0003  LP  0000  +                ',
        '0004   +   0004-0004  LP  0000  +                ',
        '0005   +   0005-0005  LP  0000  +                ',
        '0006   +I  0006-0006  H   0200  +                ',
        '0007   +I  0007-0007  H   0200  +                ',
        '0008   +I  0008-0008  H   0200  +                ',
        '0009   +I  0009-0009  H   0200  +                ',
        '000A   -I  000A-000A                             ',
        '000B   -I  000B-000B                             ',
        '000C   -I  000C-000C                             ',
        '000D   -I  000D-000D                             ',
        '000E   -I  000E-000E                             ',
        '000F   -I  000F-000F                             ',
        '',
        'CPC ND = 008562.T02.IBM.02.0000000790A8                       ',
        'CPC SI = 8562.Z06.IBM.02.00000000000790A8                     ',
        '         Model: T02                                          ',
        'CPC ID = 00                                                   ',
        'CPC NAME = T256                                               ',
        'LP NAME = S5E        LP ID = 21                               ',
        'CSS ID  = 2                                                   ',
        'MIF ID  = 1                                                   ',
        '                                                             ',
        '+ ONLINE    - OFFLINE    N NOT AVAILABLE    / MIXED STATE    ',
        'W WLM-MANAGED                                                 ',
        '                                                             ',
        'I        INTEGRATED INFORMATION PROCESSOR (zIIP)              ',
        'CPC ND  CENTRAL PROCESSING COMPLEX NODE DESCRIPTOR            ',
        'CPC SI  SYSTEM INFORMATION FROM STSI INSTRUCTION              ',
        'CPC ID  CENTRAL PROCESSING COMPLEX IDENTIFIER                 ',
        'CPC NAME CENTRAL PROCESSING COMPLEX NAME                      ',
        'LP NAME  LOGICAL PARTITION NAME                               ',
        'LP ID    LOGICAL PARTITION IDENTIFIER                         ',
        'CSS ID   CHANNEL SUBSYSTEM IDENTIFIER                         ',
        'MIF ID   MULTIPLE IMAGE FACILITY IMAGE IDENTIFIER             '
    ]

    send_command_2.message_out = ['IEE505I CORE(06),OFFLINE']
    send_command_3.message_out = ['IEE505I CORE(07),OFFLINE']
    send_command_4.message_out = ['IEE505I CORE(08),OFFLINE']
    send_command_5.message_out = ['IEE505I CORE(09),OFFLINE']

    send_command.side_effect = [send_command_1, send_command_2, send_command_3,
                                send_command_4, send_command_5]

    chaoszos.zos.actions.configure_processors(processor_type_to_change='ziip',
                                              status_to_change_to='offline',
                                              location="SYS1", secrets=secrets)

    assert send_command.call_count == 5

    send_command.assert_any_call(location="SYS1", connection_information="password1",
                                 command_to_send="D M=CORE",
                                 message_to_watch_for="IEE174I")
    send_command.assert_any_call(location="SYS1", connection_information="password1",
                                 command_to_send="CF CORE(0006),OFFLINE",
                                 message_to_watch_for="IEE505I")
    send_command.assert_any_call(location="SYS1", connection_information="password1",
                                 command_to_send="CF CORE(0007),OFFLINE",
                                 message_to_watch_for="IEE505I")
    send_command.assert_any_call(location="SYS1", connection_information="password1",
                                 command_to_send="CF CORE(0008),OFFLINE",
                                 message_to_watch_for="IEE505I")
    send_command.assert_any_call(location="SYS1", connection_information="password1",
                                 command_to_send="CF CORE(0009),OFFLINE",
                                 message_to_watch_for="IEE505I")


@patch('chaoszos.zos.actions.Send_Command', autospec=True)
def test_configure_1_ziip_core_offline(send_command):
    secrets = dict()
    secrets["SYS1"] = "password1"

    send_command_1 = MagicMock()
    send_command_2 = MagicMock()

    send_command_1.message_out = [
        'IEE174I 16.54.16 DISPLAY M 923                   ',
        'CORE STATUS: HD=Y   MT=2  MT_MODE: CP=1  zIIP=2  ',
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
        '000E   +I  001C-001D  H   0000  ++               ',
        '000F   +I  001E-001F  H   0000  ++               ',
        '',
        'CPC ND = 008562.T02.IBM.02.0000000790A8                       ',
        'CPC SI = 8562.Z06.IBM.02.00000000000790A8                     ',
        '         Model: T02                                          ',
        'CPC ID = 00                                                   ',
        'CPC NAME = T256                                               ',
        'LP NAME = S5E        LP ID = 21                               ',
        'CSS ID  = 2                                                   ',
        'MIF ID  = 1                                                   ',
        '                                                             ',
        '+ ONLINE    - OFFLINE    N NOT AVAILABLE    / MIXED STATE    ',
        'W WLM-MANAGED                                                 ',
        '                                                             ',
        'I        INTEGRATED INFORMATION PROCESSOR (zIIP)              ',
        'CPC ND  CENTRAL PROCESSING COMPLEX NODE DESCRIPTOR            ',
        'CPC SI  SYSTEM INFORMATION FROM STSI INSTRUCTION              ',
        'CPC ID  CENTRAL PROCESSING COMPLEX IDENTIFIER                 ',
        'CPC NAME CENTRAL PROCESSING COMPLEX NAME                      ',
        'LP NAME  LOGICAL PARTITION NAME                               ',
        'LP ID    LOGICAL PARTITION IDENTIFIER                         ',
        'CSS ID   CHANNEL SUBSYSTEM IDENTIFIER                         ',
        'MIF ID   MULTIPLE IMAGE FACILITY IMAGE IDENTIFIER             '

    ]

    send_command_2.message_out = ['IEE505I CORE(0E),OFFLINE']

    send_command.side_effect = [send_command_1, send_command_2]

    chaoszos.zos.actions.configure_processors(processor_type_to_change='ziip',
                                              status_to_change_to='offline',
                                              location="SYS1",
                                              secrets=secrets,
                                              processor_count_to_change=1)

    assert send_command.call_count == 2

    send_command.assert_any_call(location="SYS1", connection_information="password1",
                                 command_to_send="D M=CORE",
                                 message_to_watch_for="IEE174I")
    send_command.assert_any_call(location="SYS1", connection_information="password1",
                                 command_to_send="CF CORE(000E),OFFLINE",
                                 message_to_watch_for="IEE505I")


def test_attempt_to_configure_all_cps_offline():
    with pytest.raises(InterruptExecution) as x:
        chaoszos.zos.actions.configure_processors(processor_type_to_change="cp",
                                                  status_to_change_to='offline',
                                                  location="SYS1")
    assert 'Can not configure all CPs offline' in str(x.value)


def test_configure_invalid_processor_type_to_change():
    with pytest.raises(InterruptExecution) as x:
        chaoszos.zos.actions.configure_processors(processor_type_to_change="bob",
                                                  status_to_change_to='offline',
                                                  location="SYS1")
    assert 'Invalid processor type specified' in str(x.value)


def test_configure_empty_location_offline():
    with pytest.raises(InterruptExecution) as x:
        chaoszos.zos.actions.configure_processors(processor_type_to_change="ziip",
                                                  status_to_change_to='offline',
                                                  location="")
    assert 'No target specified for action' in str(x.value)


def test_configure_empty_secrets_offline():
    with pytest.raises(InterruptExecution) as x:
        chaoszos.zos.actions.configure_processors(processor_type_to_change='ziip',
                                                  status_to_change_to='offline',
                                                  location='SYS1')
    assert 'No secrets specified' in str(x.value)
