import rsa
import sqlite3

# Connection to SQLite3 public_Keys
conn = sqlite3.connect('../Pk_Mk/public_keys.db')
x = conn.cursor()

# Connection to SQLite3 public_Keys
connection = sqlite3.connect('Database_SKM/private_key.db')
y = connection.cursor()


def generate_keys():
    (skm_publicKey, skm_privateKey) = rsa.newkeys(2048)

    skm_publicKey_save = skm_publicKey.save_pkcs1().decode('utf-8')

    skm_privateKey_save = skm_privateKey.save_pkcs1().decode('utf-8')

    dict_users_publicKeys = {
        'SKM': skm_publicKey_save
    }

    dict_users_privateKeys = {
        'SKM': skm_privateKey_save
    }

    for item in dict_users_publicKeys.items():
        x.execute("INSERT OR IGNORE INTO publicKeys VALUES (?,?)",
                  (item[0], item[1]))
        conn.commit()

    for item in dict_users_privateKeys.items():
        y.execute("INSERT OR IGNORE INTO privateKeys VALUES (?,?)",
                  (item[0], item[1]))
        connection.commit()

    print('fatto fino qui')


def decrypt():
    y.execute("SELECT * FROM privateKeys WHERE server = ?", ('SKM',))
    user_privateKey = y.fetchall()
    privateKey_usable = rsa.PrivateKey.load_pkcs1(user_privateKey[0][1])

    with open("../message.txt", "r") as file:
        a = file.read()
        print(type(a))
        print(a)
        print()
        a = bytes(a,'unicode_escape')
        print(type(a))
        print(a)
        print()
        a = a.decode('unicode_escape').encode("raw_unicode_escape")
        print(type(a))
        print(a)
        print()
        message = rsa.decrypt(a, privateKey_usable)
        print(type(message))
        print(message)

    #with open("../message.txt", "rb") as f:
    #    crypto = f.read()
    #    print(crypto)
    #    print()
    #    message = rsa.decrypt(crypto, privateKey_usable)
    #    print(message)


if __name__ == "__main__":
    #generate_keys()
    decrypt()
