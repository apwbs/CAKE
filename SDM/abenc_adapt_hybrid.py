from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, GT
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import hashPair as sha2, deserialize, serialize
import json
import write
import sqlite3
import econders_decoders
import rsa_sdm
import random
import rsa
from pprint import pprint
import hashlib

sender_address = 'aiufhaisufhgasdoif'


class HybridABEnc(ABEnc):

    def __init__(self, scheme, groupObj):
        ABEnc.__init__(self)
        # check properties (TODO)
        self.abenc = scheme
        self.group = groupObj

    def setup(self):
        return self.abenc.setup()

    def encrypt(self, pk, M, object):
        key = self.group.random(GT)
        c1 = self.abenc.encrypt(pk, key, object)
        cipher = AuthenticatedCryptoAbstraction(sha2(key))
        c2 = cipher.encrypt(M)
        return {'c1': c1, 'c2': c2}


def main(message, access_policy, message_id):
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    hyb_abe = HybridABEnc(cpabe, groupObj)

    message = bytes(message, 'utf-8')

    (pk, mk) = hyb_abe.setup()
    pk_encoded = econders_decoders.pk_encoder(pk)
    pk_dumped = json.dumps(pk_encoded)
    mk_encoded = econders_decoders.mk_encoder(mk)
    mk_dumped = json.dumps(mk_encoded)

    message_decoded = message.decode('utf-8')
    if message_decoded.find('//') == -1:
        print('Example with one policy and one receiver')

        # Connection to SQLite3 database
        connection = sqlite3.connect('../Pk_Mk/keys.db')
        y = connection.cursor()

        y.execute("INSERT OR IGNORE INTO pkmk_keys VALUES (?,?,?)", (recipient, pk_dumped, mk_dumped))
        connection.commit()

        ct = hyb_abe.encrypt(pk, message, access_policy)
        print(ct)
        ct_encoded = econders_decoders.ciphertext_encoder(ct)
        ct_dumped = json.dumps(ct_encoded)

        # Connection to SQLite3 database
        conn = sqlite3.connect('Database_SDM/database.db')
        x = conn.cursor()

        x.execute("INSERT OR IGNORE INTO ciphertext VALUES (?,?,?,?)", (sender_address, recipient, ct_dumped, 'null'))
        conn.commit()

        write.main(sender_address, message_id, ct_dumped)
    else:
        print('I am trying this one')

        # Connection to SQLite3 database
        connection = sqlite3.connect('../Pk_Mk/keys.db')
        y = connection.cursor()
        # Connection to SQLite3 database
        conn = sqlite3.connect('Database_SDM/database.db')
        x = conn.cursor()
        # Connection to SQLite3 database
        connection1 = sqlite3.connect('../Pk_Mk/public_keys.db')
        k = connection1.cursor()

        recipients = message_id.split('//')
        case_id = random.randint(1, 2 ** 64)

        y.execute("INSERT OR IGNORE INTO pkmk_keys VALUES (?,?,?)", (str(case_id), pk_dumped, mk_dumped))
        connection.commit()

        x.execute("INSERT OR IGNORE INTO ciphertext VALUES (?,?,?,?)",
                  (sender_address, str(recipients), '', str(case_id)))
        conn.commit()
        message = message.decode('utf-8').split('//')
        access_policy = access_policy.split('//')
        list_paired = list(zip(message, access_policy, recipients))
        test_list = []

        k.execute("SELECT * FROM publicKeys WHERE server = ?", ('SKM',))
        user_publicKey = k.fetchall()
        publicKey_usable = rsa.PublicKey.load_pkcs1(user_publicKey[0][1])

        for element in list_paired:
            salt = random.randint(1, 2 ** 64)
            salt1 = str(salt).encode()
            salt_encrypted = rsa.encrypt(salt1, publicKey_usable)
            salt_encrypted_dumped = "".join(chr(i) for i in salt_encrypted)
            s_1 = element[0] + str(salt)
            s_1 = s_1.encode()
            s_1_hashed = hashlib.sha256(s_1)
            hex_dig = s_1_hashed.hexdigest()
            ct = hyb_abe.encrypt(pk, element[0], element[1])
            ct_encoded = econders_decoders.ciphertext_encoder(ct)
            ct_dumped = json.dumps(ct_encoded)
            # ct_dumped_encrypted = rsa_sdm.encrypt(ct_dumped)
            test_list.append((element[2], ct_dumped, hex_dig, salt_encrypted_dumped))

        # print(test_list)
        write.main(test_list, case_id)


if __name__ == "__main__":
    main()
