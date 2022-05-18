from charm.toolbox.pairinggroup import PairingGroup
import json
import rsa
import sqlite3


def pk_encoder(pk):
    Pk_dict = {'g': None, 'g2': None, 'h': None, 'f': None, 'e_gg_alpha': None}

    global groupObj
    groupObj = PairingGroup('SS512')

    g = pk['g']
    g = groupObj.serialize(g)
    g = g.decode('utf-8')
    Pk_dict['g'] = g

    g2 = pk['g2']
    g2 = groupObj.serialize(g2)
    g2 = g2.decode('utf-8')
    Pk_dict['g2'] = g2

    h = pk['h']
    h = groupObj.serialize(h)
    h = h.decode('utf-8')
    Pk_dict['h'] = h

    f = pk['h']
    f = groupObj.serialize(f)
    f = f.decode('utf-8')
    Pk_dict['f'] = f

    e_gg_alpha = pk['e_gg_alpha']
    e_gg_alpha = groupObj.serialize(e_gg_alpha)
    e_gg_alpha = e_gg_alpha.decode('utf-8')
    Pk_dict['e_gg_alpha'] = e_gg_alpha

    return Pk_dict


def mk_encoder(mk):
    Mk_dict = {'beta': None, 'g2_alpha': None}

    beta = mk['beta']
    beta = groupObj.serialize(beta)
    beta = beta.decode('utf-8')
    Mk_dict['beta'] = beta

    g2_alpha = mk['g2_alpha']
    g2_alpha = groupObj.serialize(g2_alpha)
    g2_alpha = g2_alpha.decode('utf-8')
    Mk_dict['g2_alpha'] = g2_alpha

    return Mk_dict


def ciphertext_encoder(ct):
    conn = sqlite3.connect('../Pk_Mk/public_keys.db')
    x = conn.cursor()

    x.execute("SELECT * FROM publicKeys WHERE server = ?", ('SKM',))
    user_publicKey = x.fetchall()
    publicKey_usable = rsa.PublicKey.load_pkcs1(user_publicKey[0][1])

    Dict = {}
    c1 = {'C_tilde': None, 'C': None, 'Cy': {}, 'Cyp': {}, 'policy': None, 'attributes': None}
    c2 = {'alg': None, 'msg': None, 'digest': None}

    Dict['c1'] = c1

    c_tilde = ct['c1']['C_tilde']
    c_tilde = groupObj.serialize(c_tilde)
    c_tilde = rsa.encrypt(c_tilde, publicKey_usable)
    c_tilde = "".join(chr(i) for i in c_tilde)
    c1['C_tilde'] = c_tilde

    c = ct['c1']['C']
    c = groupObj.serialize(c)
    c = rsa.encrypt(c, publicKey_usable)
    c = "".join(chr(i) for i in c)
    c1['C'] = c

    cy = ct['c1']['Cy']
    for u in cy:
        s = groupObj.serialize(cy[u])
        s = rsa.encrypt(s, publicKey_usable)
        s = "".join(chr(i) for i in s)
        c1['Cy'][u] = s

    cyp = ct['c1']['Cyp']
    for u in cyp:
        s = groupObj.serialize(cyp[u])
        s = rsa.encrypt(s, publicKey_usable)
        s = "".join(chr(i) for i in s)
        c1['Cyp'][u] = s

    c1['policy'] = ct['c1']['policy']
    c1['attributes'] = ct['c1']['attributes']

    Dict['c2'] = c2
    c2['alg'] = ct['c2']['alg']
    c2['msg'] = ct['c2']['msg']
    c2['digest'] = ct['c2']['digest']

    return Dict


# def ciphertext_decoder(ct_dumped):
#     Dict1 = {}
#     c1 = {'C_tilde': None, 'C': None, 'Cy': {}, 'Cyp': {}, 'policy': None, 'attributes': None}
#     c2 = {'alg': None, 'msg': None, 'digest': None}
#
#     Dict1['c1'] = c1
#
#     ct_dumped = json.loads(ct_dumped)  # ecco questo è il 'load' fatto dopo. Verrà tolto ovviamente
#     c_tilde = ct_dumped['c1']['C_tilde']
#     c_tilde = c_tilde.encode('utf-8')
#     c_tilde = groupObj.deserialize(c_tilde)
#     c1['C_tilde'] = c_tilde
#
#     c = ct_dumped['c1']['C']
#     c = c.encode('utf-8')
#     c = groupObj.deserialize(c)
#     c1['C'] = c
#
#     cy = ct_dumped['c1']['Cy']
#     for u in cy:
#         s = cy[u].encode('utf-8')
#         s = groupObj.deserialize(s)
#         c1['Cy'][u] = s
#
#     cyp = ct_dumped['c1']['Cyp']
#     for u in cyp:
#         s = cyp[u].encode('utf-8')
#         s = groupObj.deserialize(s)
#         c1['Cyp'][u] = s
#
#     c1['policy'] = ct_dumped['c1']['policy']
#     c1['attributes'] = ct_dumped['c1']['attributes']
#
#     Dict1['c2'] = c2
#     c2['alg'] = ct_dumped['c2']['alg']
#     c2['msg'] = ct_dumped['c2']['msg']
#     c2['digest'] = ct_dumped['c2']['digest']
#
#     return Dict1
