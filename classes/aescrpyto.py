from Cryptodome.Cipher import AES
from Cryptodome import Random
import base64


class AESCrpyto:

    def __init__(self, keyandnonce=""):
        if keyandnonce:
            arr = keyandnonce.split(".")
            self.key = base64.b64decode(arr[0].encode())
            self.nonce = base64.b64decode(arr[1].encode())
        else:
            self.key = Random.get_random_bytes(16)
            cipher = AES.new(self.key, AES.MODE_EAX)
            self.nonce = cipher.nonce

    def encode(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX, self.nonce)
        return cipher.encrypt_and_digest(data)[0]

    def decode(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX, self.nonce)
        return cipher.decrypt(data)

    def getKeyAndNonce(self):
        return base64.b64encode(self.key).decode() + "." + base64.b64encode(self.nonce).decode()
