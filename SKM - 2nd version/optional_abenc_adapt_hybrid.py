from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, GT
import json
import sqlite3
import decoders_encoders

# gli attributi sono da andare a chiedere allo Smart Contract
attributes = ['9549549', '1515', '787987', '4904']


class HybridABEnc(ABEnc):

    def __init__(self, scheme, groupObj):
        ABEnc.__init__(self)
        # check properties (TODO)
        self.abenc = scheme
        self.group = groupObj

    def setup(self):
        return self.abenc.setup()

    def keygen(self, pk, mk, object):
        return self.abenc.keygen(pk, mk, object)


def main(message):
    global groupObj
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    hyb_abe = HybridABEnc(cpabe, groupObj)

    # Connection to SQLite3 database1
    connection = sqlite3.connect('../Pk_Mk/keys.db')
    y = connection.cursor()

    y.execute("SELECT * FROM pkmk_keys WHERE recipient_address = ?", (message[1],))
    keys_data = y.fetchall()

    pk_data_dumped = keys_data[0][1]
    pk = decoders_encoders.pk_decoder(pk_data_dumped)

    mk_data_dumped = keys_data[0][2]
    mk = decoders_encoders.mk_decoder(mk_data_dumped)
    sk = hyb_abe.keygen(pk, mk, attributes)

    sk_encoded = decoders_encoders.key_encoder(sk)
    sk_dumped = json.dumps(sk_encoded)

    sk_decoded = decoders_encoders.key_decoder(sk_dumped)  # viene fatto nel reading

    return sk_dumped

    print('\n')


if __name__ == "__main__":
    main()
