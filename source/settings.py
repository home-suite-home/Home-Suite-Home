#
# Filename: settings.py
# Date: 03/17/21
#
# Engineer: Wyatt Vining
# Contact: wyatt.vining@knights.ucf.edu
#
# Description:
#   Use this utility to create, update and read basic settings accros the project.
#


from configparser import ConfigParser

FILE = "settings.config"

class Settings:

    def __init__(self, settings_file = FILE):
        self.settings_file = settings_file

    # returns the boolean value at the section, option pair location
    def get_bool_setting(self, section_name, option_name):
        parser = ConfigParser()
        parser.read(self.settings_file)
        try:
            return parser.getboolean(section_name, option_name)
        except Exception as e:
            print(e)
            return -1

    def get_int_setting(self, section_name, option_name):
        parser = ConfigParser()
        parser.read(self.settings_file)
        try:
            return parser.getint(section_name, option_name)
        except Exception as e:
            print(e)
            return -1

    # returns string value at the section, option pair
    def get_setting(self, section_name, option_name):
        parser = ConfigParser()
        parser.read(self.settings_file)
        try:
            return parser.get(section_name, option_name)
        except Exception as e:
            print(e)
            return -1

    # changes or adds the option at the section, option pair
    # the section and option will be created if they do not exsist
    # the settings file will be created if it does not exsist
    def set_setting(self, section_name, option_name, value):
        parser = ConfigParser()
        parser.read(self.settings_file)

        if parser.has_section(section_name) is False:
            try:
                parser.add_section(section_name)
                with open(self.settings_file, "w") as configFile:
                    parser.write(configFile)
                configFile.close()
            except Exception as e:
                print(e)
                return -1

        try:
            parser.set(section_name, option_name, value)
            with open(self.settings_file, "w") as configFile:
                parser.write(configFile)
            configFile.close()
            return 1
        except Exception as e:
            print(e)
            return -1

# def main():
#     config = Settings()
#
#     config.set_setting("globals", "silence_alerts", "False")
#     print(config.get_setting("globals", "silence_alerts"))
#
#     if config.get_bool_setting("globals", "silence_alerts") is True:
#         print("alerts are silenced")
#
# if __name__ == "__main__":
#     main()
