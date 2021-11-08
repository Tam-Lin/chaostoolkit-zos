from unittest.mock import MagicMock, patch
from chaoslib.exceptions import InterruptExecution
from chaoszos.__send_zos_command import Send_Command

import zhmcclient
import zhmcclient_mock

@patch('zhmcclient.Session', spec=zhmcclient_mock.FakedSession)
def test_send_command_using_hmc():
    1/0

def test_send_command_using_ansible():
    1/0

