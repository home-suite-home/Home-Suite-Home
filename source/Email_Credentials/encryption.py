from configparser import ConfigParser
from cryptography.fernet import Fernet
import json

class Encryption:

    def setKey(self, keyFile):
        key = Fernet.generate_key()
        with open(keyFile, "wb") as keyFile:
            keyFile.write(key)

    def getKey(self, keyFile):
        with open(keyFile, "rb") as file:
            key = file.read()
        return key

    def encryptFile(self, file, key):
        fernet = Fernet(key)
        with open(file, "rb") as inFile:
            inputFile = inFile.read()

        encryptedData = fernet.encrypt(inputFile)

        with open(file, "wb") as outputFile:
            outputFile.write(encryptedData)

    def getEncryptedData(self, file, key):
        fernet = Fernet(key)

        with open(file, "rb") as encryptedFile:
            encryptedData = encryptedFile.read()

        decryptedData = fernet.decrypt(encryptedData)

        return decryptedData

class PiEmailCredentials(Encryption):

    def __init__(self, pi_creds_file, pi_key_file):
        self.pi_creds_file = pi_creds_file
        self.pi_key_file = pi_key_file

    def getPiEmail(self):
        key = self.getKey(self.pi_key_file)
        userData = self.getEncryptedData(self.pi_creds_file, key)
        parser = ConfigParser()
        parser.read_string(userData.decode("utf-8"))
        try:
            return parser.get("pi_creds", "user")
        except Exception as e:
            print(e)
            return "Failed_to_retrieve"

    def getPiEmailPassword(self):
        key = self.getKey(self.pi_key_file)
        userData = self.getEncryptedData(self.pi_creds_file, key)
        parser = ConfigParser()
        parser.read_string(userData.decode("utf-8"))
        try:
            return parser.get("pi_creds", "password")
        except Exception as e:
            print(e)
            return "Failed_to_retrieve"

    def setPiCredentials(self, pi_email, pi_password):
        # key_file = "pi_creds_key.key"
        # pi_creds_file = "pi_creds.config"

        config = ConfigParser()
        config.add_section('pi_creds')
        config.set("pi_creds", "user", pi_email)
        config.set("pi_creds", "password", pi_password)

        with open(self.pi_creds_file, "w") as configFile:
            config.write(configFile)

        self.setKey(self.pi_key_file)
        key = self.getKey(self.pi_key_file)

        self.encryptFile(self.pi_creds_file, key)

def main():
    pi_creds = PiEmailCredentials("pi_email_creds.config", "pi_key.key")
    # pi_creds.setPiCredentials("home.suite.home.test.user@gmail.com", "homeuser")

    print("Pi Email Username: ", pi_creds.getPiEmail())
    print("Pi Email Password: ", pi_creds.getPiEmailPassword())

if __name__ == "__main__":
    main()
