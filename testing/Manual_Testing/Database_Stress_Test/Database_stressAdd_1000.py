import Database

def main():

    data = Database.Database()

    for i in range(1, 101):
        sensorName = "temp_" + str(i)
        print(sensorName)
        for x in range(45000):
            data.SendSensorData(round(random.uniform(15, 30), 2), sensorName, "temperature")

if __name__ == "__main__":
    main()
