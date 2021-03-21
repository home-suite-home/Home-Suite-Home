#Engineer: Andres Graterol

import pytest 
from settings import *

setting = Settings("settings.config")

def test_booleanGetter():
    # Checking that we don't encounter any exceptions when getting the bool value
    assert (setting.get_bool_setting("alerts", "silence_alerts") != -1)

def test_intGetter():
    # Checking that we don't encounter exceptions in the alerts section 
    assert (setting.get_int_setting("alerts", "rate_limit") != -1)
    # Checking that we don't encounter excpetions in the sensors section
    assert (setting.get_int_setting("sensors", "poll_rate") != -1)

def test_settingGetter():
    # Checking that we don't encounter exceptions in all
    # section-option pairs  
    assert (setting.get_setting("alerts", "rate_limit") != -1)
    assert (setting.get_setting("alerts", "silence_alerts") != -1)
    assert (setting.get_setting("sensors", "poll_rate") != -1)