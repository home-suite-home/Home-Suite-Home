from configparser import ConfigParser
import json

class StringModifier:

    def appendStringList(self, baseList, newItem):
        newList = baseList.strip("]")
        newList += ", \""
        newList += newItem.strip()
        newList += "\"]"
        return newList

    def appendIntList(self, baseList, newItem):
        newList = baseList.strip("]")
        newList += ", "
        newList += "]"
        return newList

    def removeFromList(self, baseList, itemRemoved):
        listAsArray = json.loads(baseList)
        try:
            index = listAsArray.index(itemRemoved)
        except:
            index = -1
            print("Item not found.")
            return index
        try:
            listAsArray.remove(itemRemoved)
        except:
            print("Failed to remove item")
            index = -1
            return index
        return index

class SensorModifier(StringModifier):

    def __init__(self, configFile):
        self.configFile = configFile

    def _addSensorName(self, parser, sectionName, name):
        oldNameString = parser.get(sectionName, "sensor_name")
        oldNamesArray = json.loads(oldNameString)
        if name in oldNamesArray:
            print("failed to add, name already in use")
            return False
        newNameString = self.appendStringList(oldNameString, name)
        print(newNameString)
        parser.set(sectionName, "sensor_name", newNameString)
        with open(self.configFile, "w") as configurationFile:
            parser.write(configurationFile)
        configurationFile.close()
        return True

    def addSensor(self, sectionName, name, address, subAddress, maxThreshold, minThreshold, alerts):
        parser = ConfigParser()
        parser.read(self.configFile)

        if parser.has_section(sectionName):
            try:
                self._addSensorName(parser, sectionName, name)
            except Exception as e:
                print(e)
        else:
            print(parser.sections())


def main():
    config = SensorModifier("sensors.config")
    config.addSensor("temperature", "test sensor", "http://testSensor:233", "subAddress", 80, -10, True)
    print("sensor added")

if __name__ == "__main__":
    main()
