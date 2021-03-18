import sys
sys.path.insert(1, "../../../source")
import timeKeeper
sys.path.insert(1, "../../../source/HTTP_Component")
import Sensors
sys.path.insert(1, "../../../source/Server_Component")
import Database

def main():
    db = Database.Database()
    db.saveUser("Test User", "home.suite.home.test.user@gmail.com")

if __name__ == "__main__":
    main()
