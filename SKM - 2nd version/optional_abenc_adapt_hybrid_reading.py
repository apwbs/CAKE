from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import hashPair as sha2
from math import ceil
import json
import sqlite3
import ipfshttpclient
import decoders_encoders

sender_address = 'aiufhaisufhgasdoif'


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
            raise Exception("failed to decrypt!")
        cipher = AuthenticatedCryptoAbstraction(sha2(key))
        return cipher.decrypt(c2)


def main(message):
    global groupObj
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    hyb_abe = HybridABEnc(cpabe, groupObj)

    # Connection to SQLite3 database1
    connection1 = sqlite3.connect('../Pk_Mk/keys.db')
    y = connection1.cursor()

    y.execute("SELECT * FROM pkmk_keys WHERE recipient_address = ?", (message[1],))
    keys_data = y.fetchall()

    pk_data_dumped = keys_data[0][1]
    pk = decoders_encoders.pk_decoder(pk_data_dumped)

    sk = decoders_encoders.key_decoder(message[2])  # si usa la chiave inviata dal client

    # Connection to SQLite3 database
    connection = sqlite3.connect('../SDM/Database_SDM/database.db')
    k = connection.cursor()

    k.execute("SELECT * FROM ciphertext WHERE sender_address=? AND recipient_address=?", (sender_address, message[1]))
    ct_data = k.fetchall()
    # ct = decoders_encoders.ciphertext_decoder(ct_data[0][2])

    print('e ora decifriamo')

    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

    getfile = api.cat(ct_data[0][3])
    test = json.loads(getfile)
    test = test['content']
    test = decoders_encoders.ciphertext_decoder(test)

    mdec = hyb_abe.decrypt(pk, sk, test)

    return mdec


if __name__ == "__main__":
    main(message)
