from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, GT
import json
import sqlite3
import decoders_encoders
import company_client_skm
import SC_retrieve_link

# gli attributi sono da andare a chiedere allo Smart Contract
# attributes_test = ['10', '52', '4904']
attributes_0x11 = ['10']
attributes_0x22 = ['4904']
attributes_0x33 = ['52']
# attributes = ['FOUR', 'TWO']

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

    def keygen(self, pk, mk, object):
        return self.abenc.keygen(pk, mk, object)


"""
function that creates a key for the demanding client. The key is generated using the 
"shared secret" between the SDM and SKM, and the attributes of that particular client 
"""


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

    if message[2] == '0x6B6E4913eF67a7611De6157CfCaa782F57670d7F':
        sk = hyb_abe.keygen(pk, mk, attributes_0x11)
    elif message[2] == '0xC869a3B0Aed8121c95d2F0016E7F4bBe2a5B9754':
        sk = hyb_abe.keygen(pk, mk, attributes_0x22)
    else:
        sk = hyb_abe.keygen(pk, mk, attributes_0x33)

    # attributes = company_client_skm.retrieve_attributes(message[2])

    # Connection to SQLite3 database1
    # connectionj = sqlite3.connect('Database_SKM/attributes.db')
    # j = connectionj.cursor()
    # values_attributes = []
    # for u in attributes:
    #     j.execute("SELECT * FROM attributes WHERE key = ?", (u,))
    #     attributes_values = j.fetchall()
    #     attributes_values = attributes_values[0][1]
    #     values_attributes.append(attributes_values)

    # choose which version
    # attributes_list_string = list(map(str, attributes))
    # sk = hyb_abe.keygen(pk, mk, attributes_list_string)
    # or
    # sk = hyb_abe.keygen(pk, mk, values_attributes)

    sk_encoded = decoders_encoders.key_encoder(sk)
    sk_dumped = json.dumps(sk_encoded)

    # Connection to SQLite3 database1
    conn = sqlite3.connect('Database_SKM/database.db')
    x = conn.cursor()

    x.execute("INSERT OR IGNORE INTO keys VALUES (?,?)", (message[2], sk_dumped))
    conn.commit()

    sk_decoded = decoders_encoders.key_decoder(sk_dumped)

    # Connection to SQLite3 database
    connection = sqlite3.connect('../SDM/Database_SDM/database.db')
    k = connection.cursor()

    k.execute("SELECT * FROM ciphertext WHERE case_id=?", (message[1],))
    ct_data = k.fetchall()
    ipfs_link = ct_data[0][2]

    # ipfs_link = SC_retrieve_link.retrieve_link(message[1])
    # print(message[1])
    print(ipfs_link)

    return ipfs_link


if __name__ == "__main__":
    main()
