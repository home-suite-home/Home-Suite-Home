import sys
sys.path.insert(1, "../../../source")
import timeKeeper
sys.path.insert(1, "../../../source/HTTP_Component")
import Sensors
sys.path.insert(1, "../../../source/Server_Component")
import Database
from time import sleep

data = Database.Database()

def main():
    configs = data.GetConfigData()

    for record in configs:
        print()
        type = record["type"]
        print("type: ", type)
        name = record["name"]
        print("name: ", name)
        address = record["address"]
        print("address: ", address)
        sub_address = record["sub_address"]
        print("subaddress: ", sub_address)
        min_threshold = record["min_threshold"]
        print("min_threshold: ", min_threshold)
        max_threshold = record["max_threshold"]
        print("max_threshold: ", max_threshold)
        alerts = record["alerts"]
        print("alerts: ", alerts)
        print()


if __name__ == "__main__":
    main()
