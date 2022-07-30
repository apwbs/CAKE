from charm.toolbox.pairinggroup import PairingGroup
import json
import rsa
import sqlite3


def pk_encoder(pk):
    conn = sqlite3.connect('../Pk_Mk/public_keys.db')
    x = conn.cursor()

    x.execute("SELECT * FROM publicKeys WHERE server = ?", ('SKM',))
    user_publicKey = x.fetchall()
    publicKey_usable = rsa.PublicKey.load_pkcs1(user_publicKey[0][1])

    Pk_dict = {'g': None, 'g2': None, 'h': None, 'f': None, 'e_gg_alpha': None}

    global groupObj
    groupObj = PairingGroup('SS512')

    g = pk['g']
    g = groupObj.serialize(g)
    g = rsa.encrypt(g, publicKey_usable)
    g = "".join(chr(i) for i in g)
    Pk_dict['g'] = g

    g2 = pk['g2']
    g2 = groupObj.serialize(g2)
    g2 = rsa.encrypt(g2, publicKey_usable)
    g2 = "".join(chr(i) for i in g2)
    Pk_dict['g2'] = g2

    h = pk['h']
    h = groupObj.serialize(h)
    h = rsa.encrypt(h, publicKey_usable)
    h = "".join(chr(i) for i in h)
    Pk_dict['h'] = h

    f = pk['h']
    f = groupObj.serialize(f)
    f = rsa.encrypt(f, publicKey_usable)
    f = "".join(chr(i) for i in f)
    Pk_dict['f'] = f

    e_gg_alpha = pk['e_gg_alpha']
    e_gg_alpha = groupObj.serialize(e_gg_alpha)
    e_gg_alpha = rsa.encrypt(e_gg_alpha, publicKey_usable)
    e_gg_alpha = "".join(chr(i) for i in e_gg_alpha)
    Pk_dict['e_gg_alpha'] = e_gg_alpha

    return Pk_dict


def mk_encoder(mk):
    conn = sqlite3.connect('../Pk_Mk/public_keys.db')
    x = conn.cursor()

    x.execute("SELECT * FROM publicKeys WHERE server = ?", ('SKM',))
    user_publicKey = x.fetchall()
    publicKey_usable = rsa.PublicKey.load_pkcs1(user_publicKey[0][1])

    Mk_dict = {'beta': None, 'g2_alpha': None}

    beta = mk['beta']
    beta = groupObj.serialize(beta)
    beta = rsa.encrypt(beta, publicKey_usable)
    beta = "".join(chr(i) for i in beta)
    Mk_dict['beta'] = beta

    g2_alpha = mk['g2_alpha']
    g2_alpha = groupObj.serialize(g2_alpha)
    g2_alpha = rsa.encrypt(g2_alpha, publicKey_usable)
    g2_alpha = "".join(chr(i) for i in g2_alpha)
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

    b = ct['c1']['policy']
    b = rsa.encrypt(bytes(b, 'utf-8'), publicKey_usable)
    b = "".join(chr(i) for i in b)
    c1['policy'] = b
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
