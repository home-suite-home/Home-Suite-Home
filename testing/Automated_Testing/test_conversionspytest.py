# Engineer: Andres Graterol 

from conversions import *
import pytest

def test_tempConvert():
    unit = Units("temperature", "fahrenheit")
    unit_2 = Units("temperature", "f")
    unit_3 = Units("temperature", "F")
    unit_4 = Units("temperature", "imperial")
    unit_5 = Units("temperature", "celsius")

    assert(unit.convert(50) == 122)
    assert(unit_2.convert(42) == 107.6)
    assert(unit_3.convert(22) == 71.6)
    assert(unit_4.convert(20) == 68)
    assert(unit_5.convert(57) == 57)

def test_lightConvert():
    unit = Units("light", "lumens")
    unit_2 = Units("light", "lm")
    unit_3 = Units("light", "lum") 
    unit_4 = Units("light", "imperial")
    unit_5 = Units("light", "foot-candle")
    unit_6 = Units("light", "tons of refridgeration")

    assert(unit.convert(12) == 1.11)
    assert(unit_2.convert(60) == 5.57)
    assert(unit_3.convert(800) == 74.32)
    assert(unit_4.convert(1800) == 167.23)
    assert(unit_5.convert(75) == 6.97)
    assert(unit_6.convert(98) == 98)

def test_pressureConvert():
    unit = Units("barometeric", "kpa")
    unit_2 = Units("barometer", "kilopascale")
    unit_3 = Units("pressure", "bar")
    unit_4 = Units("barometeric", "atm")
    unit_5 = Units("barometer", "atmosphere")
    unit_6 = Units("pressure", "mmhg")
    unit_7 = Units("barometeric", "torr")
    unit_8 = Units("barometer", "psi")
    unit_9 = Units("pressure", "imperial")
    unit_10 = Units("barometeric", "pa")

    assert(unit.convert(200) == 0.20)
    assert(unit_2.convert(500) == 0.50)
    assert(unit_3.convert(2000) == 0.02)
    assert(unit_4.convert(6500) == 0.06)
    assert(unit_5.convert(8000) == 0.08)
    assert(unit_6.convert(620) == 4.65)
    assert(unit_7.convert(780) == 5.85)
    assert(unit_8.convert(7200) == 1.04)
    assert(unit_9.convert(4783) == 0.69)
    assert(unit_10.convert(420) == 420)

def test_altitudeConvert():
    unit = Units("altitude", "foot")
    unit_2 = Units("altitude", "feet")
    unit_3 = Units("altitude", "meters")

    assert(unit.convert(12) == 39.37)
    assert(unit_2.convert(28) == 91.86)
    assert(unit_3.convert(16) == 16)

def test_humidityConvert():
    unit = Units("humidity", "percent")

    assert(unit.convert(52) == 52) 

def test_leakConvert():
    unit = Units("leak", "ADU")

    assert(unit.convert(14) == 14)

def test_tvocConvert():
    unit = Units("tvoc", "ppb")

    assert(unit.convert(17) == 17)

def test_co2Convert():
    unit = Units("co2", "ppm")

    assert(unit.convert(28) == 28)