#
# Basic utility for converting units
#
# NOTE:
#   For all supported sensors - Need to add a private conversion Function
#   For all unsupported sensors - default is to just return the value
#

class Units:

    def __init__(self, type, units):
        self.type = type.lower()
        self.units = units.lower()
        self.units_string = units.lower()

    def convert(self, value):
        if self.type == "temperature":
            return self.__convert_temperature(value)
        elif self.type == "light":
            return self.__convert_light(value)
        elif self.type == "barometeric" or self.type == "barometer" or self.type == "pressure":
            return self.__convert_pressure(value)
        elif self.type == "humidity":
            return self.__convert_humidity(value)
        elif self.type == "leak":
            return self.__convert_leak(value)
        else:
            return value

    def convert_to_string(self, value):
        converted_string = str(self.convert(value))
        converted_string += " "
        converted_string += self.units_string
        return converted_string


    def __convert_temperature(self, value):
        if self.units == "fahrenheit" or self.units == "f" or self.units == "imperial":
            degrees_f = (value * (9.0/5.0)) + 32
            degrees_f = round(degrees_f, 2)
            self.units_string = "F"
            return degrees_f
        else:
            self.units_string = "C"
            return value


    def __convert_light(self, value):
        if self.units == "lumens" or self.units == "lm" or self.units == "lum" or self.units == "imperial":
            lumens = value * 0.09290304; # constant for conversion
            lumens = round(lumens, 2)
            self.unit_string = "lm"
            return lumens
        elif self.units == "foot-candle":
            foot_candles = value / 10.764
            foot_candles = round(foot_candles, 2)
            self.unit_string = "fc"
            return foot_candles
        else:
            self.units_string = "lx"
            return value


    def __convert_pressure(self, value):
        if self.units == "kpa" or "kilopascale" in self.units:
            kpa = value / 1000
            kap = round(kpa, 2)
            self.units_string = "kPa"
            return kpa
        elif self.units == "bar":
            bar = value / 100000
            bar = round(bar, 2)
            self.units_string = "bar"
            return bar
        elif self.units == "atm" or "atmosphere" in self.units:
            atm = value / 101325
            atm = round(atm, 2)
            self.units_string = "atm"
            return atm
        elif self.units == "mmhg" or self.units == "torr":
            mmhg = value / 133.322
            mmhg = round(mmhg, 2)
            self.units_string = "mmHg"
            return mmhg
        elif self.units == "psi" or self.units == "imperial":
            psi = value / 6894.7572931783
            psi = round(psi, 2)
            self.units_string = "psi"
            return psi
        else:
            self.units_string = "Pa"
            return value


    def __convert_altitde(self, value):
        if "foot" in self.units or "feet" in self.units:
            feet = value / 0.3048
            feet = round(feet, 2)
            self.units_string = "ft"
            return feet
        else:
            self.units_string = "m"
            return value


    def __convert_humidity(self, value):
        self.unit_string = "%%"
        return value


    def __convert_leak(self, value):
        self.unit_string = "ADU"
        return value
