#python3 -m pip install pip install pycryptodome
import sqlite3
from Crypto.PublicKey import RSA

def generate_keys():
    # Connection to SQLite3 public_Keys
    conn = sqlite3.connect('Database_Reader/public_key.db')
    x = conn.cursor()

    # Connection to SQLite3 public_Keys
    connection = sqlite3.connect('Database_Reader/private_key.db')
    y = connection.cursor()

    keyPair = RSA.generate(bits=2048)

    x.execute("INSERT OR IGNORE INTO publicKeys VALUES (?,?,?)",
                  ('0xA5dfE42d5BE39A3aE6c45ED7aBbCD77F8647D54B', str(keyPair.n), str(keyPair.e)))
    conn.commit()

    y.execute("INSERT OR IGNORE INTO privateKeys VALUES (?,?,?)",
                  ('0xA5dfE42d5BE39A3aE6c45ED7aBbCD77F8647D54B', str(keyPair.n), str(keyPair.d)))
    connection.commit()

    print(type(keyPair.n))
    print(keyPair.n)
    print(hex(keyPair.n))
    exit()

    print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
    print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")



#msg = b'A message for signing'
#msg = b'123'
#from hashlib import sha512
#hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
#signature = pow(hash, keyPair.d, keyPair.n)
#print("Signature:", hex(signature))



# RSA verify signature
#msg = b'A message for signing'
#msg = b'123'
#hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
#hashFromSignature = pow(signature, keyPair.e, keyPair.n)
#print("Signature valid:", hash == hashFromSignature)

if __name__ == "__main__":
    generate_keys()
    #encrypt()