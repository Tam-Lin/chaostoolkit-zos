from unittest.mock import MagicMock, patch

from chaoszos.zos.probes import is_responding


@patch('chaoszos.zos.probes.Send_Command', autospec=True)
def test_is_responding_works(send_command):
    secrets = dict()
    secrets["SYS1"] = "password1"

    send_command_1 = MagicMock()

    send_command_1.message_out = [
        '        IEE112I 15.55.21 PENDING REQUESTS 376                        ',
        '        RM=19   IM=0     CEM=0     EM=0     RU=0    IR=0    AMRF     ',
        '        ID:R/K     T SYSNAME  MESSAGE TEXT                           ',
        '        289 R S56      *289 GEO2669A Reply one of the options        ',
        '        170 R S50      *170 DSI802A CNMM1    REPLY WITH VALID NCCF   ',
        '                       SYSTEM OPERATOR COMMAND                       ',
        '        186 R S51      *186 DSI802A CNMM2    REPLY WITH VALID NCCF   ',
        '                       SYSTEM OPERATOR COMMAND                       '
    ]

    send_command.side_effect = send_command_1

    responding = is_responding(location="SYS1", secrets=secrets)

    assert responding is True

    send_command.assert_any_call(location="SYS1",
                                 connection_information="password1",
                                 command_to_send="D R,R",
                                 message_to_watch_for="IEE112I")
