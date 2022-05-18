from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import hashPair as sha2
import json
import sqlite3
import ipfshttpclient
import decoders_encoders
import re
import rsa
import SC_retrieve_link

sender_address = 'aiufhaisufhgasdoif'

"""
Necessary ABE connections
"""


class HybridABEnc(ABEnc):
    def __init__(self, scheme, groupObj):
        ABEnc.__init__(self)
        # check properties (TODO)
        self.abenc = scheme
        self.group = groupObj

    def setup(self):
        return self.abenc.setup()

    def decrypt(self, pk, sk, ct):
        c1, c2 = ct['c1'], ct['c2']
        key = self.abenc.decrypt(pk, sk, c1)
        if key is False:
            return b' '
            # raise Exception("failed to decrypt!")
        cipher = AuthenticatedCryptoAbstraction(sha2(key))
        return cipher.decrypt(c2)


"""
"""


def main(message):
    global groupObj
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    hyb_abe = HybridABEnc(cpabe, groupObj)

    # Connection to SQLite3 public_Keys
    connection = sqlite3.connect('Database_SKM/private_key.db')
    b = connection.cursor()

    b.execute("SELECT * FROM privateKeys WHERE server = ?", ('SKM',))
    user_privateKey = b.fetchall()
    privateKey_usable = rsa.PrivateKey.load_pkcs1(user_privateKey[0][1])

    # Connection to SQLite3 database1
    connection1 = sqlite3.connect('../Pk_Mk/keys.db')
    y = connection1.cursor()

    y.execute("SELECT * FROM pkmk_keys WHERE recipient_address = ?", (message[2],))
    keys_data = y.fetchall()

    pk_data_dumped = keys_data[0][1]
    pk = decoders_encoders.pk_decoder(pk_data_dumped)

    # Connection to SQLite3 database
    conn = sqlite3.connect('Database_SKM/database.db')
    x = conn.cursor()

    x.execute("SELECT * FROM keys WHERE requester_address=?", (message[1],))
    sk_data = x.fetchall()
    sk = decoders_encoders.key_decoder(sk_data[0][1])

    # # Connection to SQLite3 database
    # connection = sqlite3.connect('../SDM/Database_SDM/database.db')
    # k = connection.cursor()

    # k.execute("SELECT * FROM ciphertext WHERE case_id=?", (message[2],))
    # ct_data = k.fetchall()
    # ct_data_check = ct_data[0][1]

    ct_data_check = SC_retrieve_link.retrieve_link(message[2])
    print(ct_data_check)
    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    getfile = api.cat(ct_data_check)
    find_separator = [m.start() for m in re.finditer(b'--->', getfile)]
    if len(find_separator) == 0:
        print('un solo messaggio')
        test = json.loads(getfile)
        check_requester = test['message_id']
        if check_requester == message[3]:
            test1 = test['content']
            test1 = decoders_encoders.ciphertext_decoder(test1)
            mdec = hyb_abe.decrypt(pk, sk, test1)
            salt = test['salt']
            salt = bytes(salt, 'unicode_escape')
            salt = salt.decode('unicode_escape').encode("raw_unicode_escape")
            salt = rsa.decrypt(salt, privateKey_usable)
            return mdec, salt
    else:
        for i in range(len(find_separator) + 1):
            if i == 0:
                check = getfile[:find_separator[i]]
            elif i < len(find_separator):
                check = getfile[find_separator[i - 1] + 4:find_separator[i]]
            else:
                check = getfile[find_separator[i - 1] + 4:]
            test = json.loads(check)
            check_requester = test['message_id']
            if check_requester == message[3]:
                test1 = test['content']
                test1 = decoders_encoders.ciphertext_decoder(test1)
                mdec = hyb_abe.decrypt(pk, sk, test1)
                salt = test['salt']
                salt = bytes(salt, 'unicode_escape')
                salt = salt.decode('unicode_escape').encode("raw_unicode_escape")
                salt = rsa.decrypt(salt, privateKey_usable)
                if mdec == b' ':
                    return mdec, b'you cannot access that data'
                return mdec, salt


# if __name__ == "__main__":
#     main(message)
