import Database
import Sensors

def main():

    data = Database.Database()
    # data.clear()

    print(data.getAvgVal("temp_50"))

if __name__ == "__main__":
    main()
