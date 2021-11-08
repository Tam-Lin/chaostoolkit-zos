from unittest.mock import MagicMock, patch
from chaoslib.exceptions import InterruptExecution
from chaoszos.zos.actions import (configure_processors)

import pytest

def test_configure_processor_offline():
    configure_processors(processor_type='cp', status='offline', location="SYS1")
    1/0

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
        configure_processors(processor_type="bob", status='offline', location="SYS1")
    assert 'No target specified for action' in str(x.value)
