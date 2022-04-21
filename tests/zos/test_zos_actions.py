from unittest.mock import MagicMock, patch

import chaoszos.zos.actions
from chaoslib.exceptions import InterruptExecution
from chaoszos.zos.actions import configure_processors
from chaoszos.__send_zos_command import Send_Command

import pytest

@patch('chaoszos.zos.actions.Send_Command', autospec=True)
def test_configure_all_ziip_cores_offline(send_command):

    secrets = dict()
    secrets["SYS1"] = "password1"

    send_command_1 = MagicMock()
    send_command_2 = MagicMock()
    send_command_3 = MagicMock()

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
'000F   +I  001E-001F  H   0000  ++               '
        ]

    send_command_2.message_out = ['IEE505I CORE(0E),OFFLINE']

    send_command_3.message_out = ['IEE505I CORE(0F),OFFLINE']

    send_command.side_effect = [send_command_1, send_command_2, send_command_3]

    configure_processors(processor_type='ziip', status='offline', location="SYS1", secrets=secrets)

    # assert send_command.call_count == 3

    send_command.assert_any_call(location="SYS1", connection_information="password1", command_to_send="D M=CORE", message_to_watch_for="IEE174I")
    send_command.assert_any_call(location="SYS1", connection_information="password1", command_to_send="CF CORE(000E),OFFLINE", message_to_watch_for="IEE505I")
    send_command.assert_any_call(location="SYS1", connection_information="password1", command_to_send="CF CORE(000F),OFFLINE", message_to_watch_for="IEE505I")

# def test_configure_cpu_offline(send_command_init):
#
#     send_command_init.return_value = True
#
#     configure_processors(processor_type='ziip', status='offline', location="SYS1")

def test_configure_all_cps_offline():
    with pytest.raises(InterruptExecution) as x:
        configure_processors(processor_type="cp", status='offline', location="SYS1")
    assert 'Can not configure all CPs offline' in str(x.value)

def test_configure_invalid_processor_type():
    with pytest.raises(InterruptExecution) as x:
        configure_processors(processor_type="bob", status='offline', location="SYS1")
    assert 'Invalid processor type specified' in str(x.value)

def test_configure_empty_location_offline():
    with pytest.raises(InterruptExecution) as x:
        configure_processors(processor_type="ziip", status='offline', location="")
    assert 'No target specified for action' in str(x.value)

# def test_configure_empty_secrets_offline():
#     with pytest.raises(KeyError) as x:
#         configure_processors(processor_type='ziip', status='offline', location='SYS1')