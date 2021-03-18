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
        else:
            return value


    def __convert_temperature(self, value):
        if self.units == "fahrenheit" or self.units == "f" or self.units == "F" or self.units == "imperial":
            return (value * (9.0/5.0)) + 32
        else:
            return value
