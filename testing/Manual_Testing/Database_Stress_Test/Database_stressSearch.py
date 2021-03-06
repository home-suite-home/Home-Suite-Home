import Database
import Sensors

def main():

    data = Database.Database()
    # data.Clear()

    print(data.GetAvgVal("temp_50"))

if __name__ == "__main__":
    main()
