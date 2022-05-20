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

    ipfs_link = SC_retrieve_link.retrieve_link(message[1])
    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    print(api)
    getfile = api.cat(ipfs_link)
    find_separator_header = [m.start() for m in re.finditer(b'---\n---', getfile)]
    check = getfile[:find_separator_header[0]]
    test = json.loads(check)
    pk_encrypted = test['pk']
    pk = decoders_encoders.pk_decoder(pk_encrypted)

    # message[3] = json.loads(message[3])
    sk = decoders_encoders.key_decoder(message[3])

    find_separator = [m.start() for m in re.finditer(b'--->', getfile)]
    find_separator_header = [m.start() for m in re.finditer(b'---\n---', getfile)]
    if len(find_separator) == 0:
        print('un solo messaggio')
        test = json.loads(getfile)
        check_requester = test['message_id']
        if check_requester == message[2]:
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
                check = getfile[find_separator_header[0]+8:find_separator[i]]
            elif i < len(find_separator):
                check = getfile[find_separator[i - 1] + 4:find_separator[i]]
            else:
                check = getfile[find_separator[i - 1] + 4:]
            test = json.loads(check)
            check_requester = test['message_id']
            if check_requester == message[2]:
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
