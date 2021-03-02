import Database
import Sensors

def main():

    data = Database.Database()
    # data.Clear()

    print(data.GetAvgVal("Indoor Temperature"))

if __name__ == "__main__":
    main()
