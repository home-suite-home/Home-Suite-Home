
# Manual Test for Database password encryption
import sys
sys.path.append("../../../source/Server_Component/")

from Database import Database

def main():
    db = Database()


    db.saveCredentials("natkingcole67@aol.com", "passw0rd")

    result1 = db.getCredentials()

    client = mongo.MongoClient()
    coll = client['sensorsdb']['creds']
    result2 = coll.find_one({})

    print(result1)
    print('')
    print(result2)



if __name__ == "__main__":
    # execute only if run as a script
    main()
