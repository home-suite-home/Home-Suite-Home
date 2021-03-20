#
# Basic utility for converting units
#
# NOTE:
#   For all supported sensors - Need to add a private conversion Function
#   For all unsupported sensors - default is to just return the value
#

class Units:

    def __init__(self, type, units):
        self.type = type
        self.units = units

    def convert(self, value):
        if self.type == "temperature":
            return self.__convert_temperature(value)
        elif self.type == "light":
            return self.__convert_light(value)
        elif self.type == "barometeric" or self.type == "barometer" or self.type == "pressure":
            return self.__convert_pressure(value)
        else:
            return value

    def convert_to_string(self, value):
        converted_string = str(self.convert(value))
        convertedString += " "
        converted_string += self.units
        return converted_string


    def __convert_temperature(self, value):
        if self.units == "fahrenheit" or self.units == "f" or self.units == "F" or self.units == "imperial":
            degrees_f = (value * (9.0/5.0)) + 32
            degrees_f = round(degrees_f, 2)
            self.units = "F"
            return degrees_f
        else:
            self.units = "C"
            return value


    def __convert_light(self, value):
        if self.units == "lumens" or self.units == "lm" or self.units == "lum" or self.units == "imperial":
            lumens = value * 0.09290304; # constant for conversion
            lumens = round(lumens, 2)
            self.unit = "lm"
            return lumens
        elif self.units == "foot-candle":
            foot_candles = value / 10.764
            foot_candles = round(foot_candles, 2)
            self.unit = "fc"
            return foot_candles
        else:
            self.units = "lx"
            return value
