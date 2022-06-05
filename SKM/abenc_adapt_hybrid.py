from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.toolbox.pairinggroup import PairingGroup, GT
import json
import decoders_encoders
import company_client_skm
import SC_retrieve_link
import ipfshttpclient
import re


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

    ipfs_link = SC_retrieve_link.retrieve_link(message[1])
    print(ipfs_link)
    api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    print(api)
    getfile = api.cat(ipfs_link)
    find_separator_header = [m.start() for m in re.finditer(b'---\n---', getfile)]
    check = getfile[:find_separator_header[0]]
    test = json.loads(check)
    pk_encrypted = test['pk']
    pk = decoders_encoders.pk_decoder(pk_encrypted)
    mk_encrypted = test['mk']
    mk = decoders_encoders.mk_decoder(mk_encrypted)

    attributes = company_client_skm.retrieve_attributes(message[2])

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
    attributes_list_string = list(map(str, attributes))
    sk = hyb_abe.keygen(pk, mk, attributes_list_string)
    # or
    # sk = hyb_abe.keygen(pk, mk, values_attributes)

    sk_encoded = decoders_encoders.key_encoder(sk)
    sk_dumped = json.dumps(sk_encoded)

    return ipfs_link, sk_dumped


# if __name__ == "__main__":
#     main()
