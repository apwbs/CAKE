from email import message
import rsa
import sqlite3

receiver = 'SKM'


def generate_keys():
    # Connection to SQLite3 public_Keys
    conn = sqlite3.connect('../Pk_Mk/public_keys.db')
    x = conn.cursor()

    # Connection to SQLite3 public_Keys
    connection = sqlite3.connect('Database_SDM/private_key.db')
    y = connection.cursor()

    (sdm_publicKey, sdm_privateKey) = rsa.newkeys(2048)

    sdm_publicKey_save = sdm_publicKey.save_pkcs1().decode('utf-8')

    sdm_privateKey_save = sdm_privateKey.save_pkcs1().decode('utf-8')

    dict_users_publicKeys = {
        'SDM': sdm_publicKey_save
    }

    dict_users_privateKeys = {
        'SDM': sdm_privateKey_save
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


def encrypt():
    message = b'3:c9rmvBmgVAURGMTdswcXF+iaU2qJwJpMWhVtRESe2HG+SlfB/gCB5EXFnVMQsdnCQZDvL7FmvfsuvQpMJMZy1Ep9d15xkUMxc3ODbUP1oyTcsQOG3AXDmSAGoWzPjpqzoIBHMG2DHDUbmyGYYBIJXGetdP1xgiSPzRJLtx0Oar4='
    conn = sqlite3.connect('../Pk_Mk/public_keys.db')
    x = conn.cursor()

    x.execute("SELECT * FROM publicKeys WHERE server = ?", (receiver,))
    user_publicKey = x.fetchall()
    publicKey_usable = rsa.PublicKey.load_pkcs1(user_publicKey[0][1])

    print(type(message))
    print(message)
    print()
    crypto = rsa.encrypt(message, publicKey_usable)
    #print(type(crypto))
    #print(crypto)
    #print('\n' + '\n')

    alisudfh = "".join(chr(i) for i in crypto)
    print(type(alisudfh))
    print(alisudfh)



    #crypto = crypto.decode('unicode_escape')
    #print(type(crypto))
    #print(crypto)
    #exit()

    with open('../message.txt', 'w') as the_file:
        the_file.write(alisudfh)

    #with open('../message.txt', 'wb') as the_file1:
    #    the_file1.write(crypto)


if __name__ == "__main__":
    #generate_keys()
    encrypt()
