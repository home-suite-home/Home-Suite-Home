# Nathan Moulton
# Security

import os

from pymongo import MongoClient
from pymongo.encryption import (Algorithm, ClientEncryption)
#from pymongo.encryption_options import AutoEncryptionOpts



class Security:
    def __init__(self, client_connection):
        self.client = client_connection
        self.client_encryption = None


    def setup(self):
        path = "lmk.txt"

        if os.path.exists(path):
            print("oh no.")
            with open(path, "rb") as f:
                local_master_key = f.read()
        else:
            local_master_key = os.urandom(96)
            with open(path, "wb") as f:
                f.write(local_master_key)

        kms_providers = {"local": {"key": local_master_key}}
        client = self.client

        # The MongoDB namespace (db.collection) used to store
        # the encryption data keys.
        key_vault_namespace = "encryption.__homeSuiteKeyVault"
        key_vault_db_name, key_vault_coll_name = key_vault_namespace.split(".", 1)

        # The MongoClient used to read/write application data.
        #client = MongoClient()
        #coll = client.test.coll
        # Clear old data
        #coll.drop()

        # Set up the key vault (key_vault_namespace) for this example.
        key_vault = client[key_vault_db_name][key_vault_coll_name]
        # Ensure that two data keys cannot share the same keyAltName.
        #key_vault.drop()
        key_vault.create_index(
            "keyAltNames",
            unique=True,
            partialFilterExpression={"keyAltNames": {"$exists": True}})

        client_encryption = ClientEncryption(
            kms_providers,
            key_vault_namespace,
            client,
            client.codec_options)

        self.client_encryption = client_encryption


    def getEncryptedField(self,field,num):

        data_key_id = self.client_encryption.create_data_key(
            'local', key_alt_names=['key' + str(num)])

        encrypted_field = self.client_encryption.encrypt(
            field,
            Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
            key_id=data_key_id)

        return encrypted_field

    def getDecryptedField(self, field):
        return self.client_encryption.decrypt(field)

    def clearKey(self):
        client['encryption']['__homeSuiteKeyVaultite'].delete_one({})
