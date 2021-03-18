import sys
sys.path.insert(1, "../../../source")
import timeKeeper
sys.path.insert(1, "../../../source/HTTP_Component")
import Sensors
sys.path.insert(1, "../../../source/Server_Component")
import Database

def main():
    db = Database.Database()
    db.saveCredentials("home.suite.home.test.user@gmail.com", "homeuser")
    record = db.getCredentials()
    print("username: ", record["email"])
    print("password: ", record["password"])

if __name__ == "__main__":
    main()
