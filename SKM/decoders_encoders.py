from charm.toolbox.pairinggroup import PairingGroup
import json
import sqlite3
import rsa
import ast


def pk_decoder(pk_data_dumped):
    # Connection to SQLite3 public_Keys
    connection = sqlite3.connect('Database_SKM/private_key.db')
    y = connection.cursor()

    y.execute("SELECT * FROM privateKeys WHERE server = ?", ('SKM',))
    user_privateKey = y.fetchall()
    privateKey_usable = rsa.PrivateKey.load_pkcs1(user_privateKey[0][1])

    Pk_dict_dec = {'g': None, 'g2': None, 'h': None, 'f': None, 'e_gg_alpha': None}

    global groupObj
    groupObj = PairingGroup('SS512')

    pk_data_dumped = json.loads(pk_data_dumped)

    g = pk_data_dumped['g']
    g = bytes(g, 'unicode_escape')
    g = g.decode('unicode_escape').encode("raw_unicode_escape")
    g = rsa.decrypt(g, privateKey_usable)
    g = groupObj.deserialize(g)
    Pk_dict_dec['g'] = g

    g2 = pk_data_dumped['g2']
    g2 = bytes(g2, 'unicode_escape')
    g2 = g2.decode('unicode_escape').encode("raw_unicode_escape")
    g2 = rsa.decrypt(g2, privateKey_usable)
    g2 = groupObj.deserialize(g2)
    Pk_dict_dec['g2'] = g2

    h = pk_data_dumped['h']
    h = bytes(h, 'unicode_escape')
    h = h.decode('unicode_escape').encode("raw_unicode_escape")
    h = rsa.decrypt(h, privateKey_usable)
    h = groupObj.deserialize(h)
    Pk_dict_dec['h'] = h

    f = pk_data_dumped['f']
    f = bytes(f, 'unicode_escape')
    f = f.decode('unicode_escape').encode("raw_unicode_escape")
    f = rsa.decrypt(f, privateKey_usable)
    f = groupObj.deserialize(f)
    Pk_dict_dec['f'] = f

    e_gg_alpha = pk_data_dumped['e_gg_alpha']
    e_gg_alpha = bytes(e_gg_alpha, 'unicode_escape')
    e_gg_alpha = e_gg_alpha.decode('unicode_escape').encode("raw_unicode_escape")
    e_gg_alpha = rsa.decrypt(e_gg_alpha, privateKey_usable)
    e_gg_alpha = groupObj.deserialize(e_gg_alpha)
    Pk_dict_dec['e_gg_alpha'] = e_gg_alpha

    return Pk_dict_dec


def mk_decoder(mk_data_dumped):
    # Connection to SQLite3 public_Keys
    connection = sqlite3.connect('Database_SKM/private_key.db')
    y = connection.cursor()

    y.execute("SELECT * FROM privateKeys WHERE server = ?", ('SKM',))
    user_privateKey = y.fetchall()
    privateKey_usable = rsa.PrivateKey.load_pkcs1(user_privateKey[0][1])

    Mk_dict_dec = {'beta': None, 'g2_alpha': None}

    mk_data_dumped = json.loads(mk_data_dumped)

    beta = mk_data_dumped['beta']
    beta = bytes(beta, 'unicode_escape')
    beta = beta.decode('unicode_escape').encode("raw_unicode_escape")
    beta = rsa.decrypt(beta, privateKey_usable)
    beta = groupObj.deserialize(beta)
    Mk_dict_dec['beta'] = beta

    g2_alpha = mk_data_dumped['g2_alpha']
    g2_alpha = bytes(g2_alpha, 'unicode_escape')
    g2_alpha = g2_alpha.decode('unicode_escape').encode("raw_unicode_escape")
    g2_alpha = rsa.decrypt(g2_alpha, privateKey_usable)
    g2_alpha = groupObj.deserialize(g2_alpha)
    Mk_dict_dec['g2_alpha'] = g2_alpha

    return Mk_dict_dec


def ciphertext_decoder(ct_dumped):
    # Connection to SQLite3 public_Keys
    connection = sqlite3.connect('Database_SKM/private_key.db')
    y = connection.cursor()

    y.execute("SELECT * FROM privateKeys WHERE server = ?", ('SKM',))
    user_privateKey = y.fetchall()
    privateKey_usable = rsa.PrivateKey.load_pkcs1(user_privateKey[0][1])

    Dict1 = {}
    c1 = {'C_tilde': None, 'C': None, 'Cy': {}, 'Cyp': {}, 'policy': None, 'attributes': None}
    c2 = {'alg': None, 'msg': None, 'digest': None}

    Dict1['c1'] = c1

    ct_dumped = json.loads(ct_dumped)
    c_tilde = ct_dumped['c1']['C_tilde']
    c_tilde = bytes(c_tilde, 'unicode_escape')
    c_tilde = c_tilde.decode('unicode_escape').encode("raw_unicode_escape")
    c_tilde = rsa.decrypt(c_tilde, privateKey_usable)
    c_tilde = groupObj.deserialize(c_tilde)
    c1['C_tilde'] = c_tilde

    c = ct_dumped['c1']['C']
    c = bytes(c, 'unicode_escape')
    c = c.decode('unicode_escape').encode("raw_unicode_escape")
    c = rsa.decrypt(c, privateKey_usable)
    c = groupObj.deserialize(c)
    c1['C'] = c

    cy = ct_dumped['c1']['Cy']
    for u in cy:
        s = cy[u]
        s = bytes(s, 'unicode_escape')
        s = s.decode('unicode_escape').encode("raw_unicode_escape")
        s = rsa.decrypt(s, privateKey_usable)
        s = groupObj.deserialize(s)
        c1['Cy'][u] = s

    cyp = ct_dumped['c1']['Cyp']
    for u in cyp:
        s = cyp[u]
        s = bytes(s, 'unicode_escape')
        s = s.decode('unicode_escape').encode("raw_unicode_escape")
        s = rsa.decrypt(s, privateKey_usable)
        s = groupObj.deserialize(s)
        c1['Cyp'][u] = s

    b = ct_dumped['c1']['policy']
    b = bytes(b, 'unicode_escape')
    b = b.decode('unicode_escape').encode("raw_unicode_escape")
    b = rsa.decrypt(b, privateKey_usable)
    b = b.decode('utf-8')
    c1['policy'] = b
    c1['attributes'] = ct_dumped['c1']['attributes']

    Dict1['c2'] = c2
    c2['alg'] = ct_dumped['c2']['alg']
    c2['msg'] = ct_dumped['c2']['msg']
    c2['digest'] = ct_dumped['c2']['digest']

    return Dict1


def key_decoder(sk_dumped):
    Dict1 = {'D': None, 'Dj': {}, 'Djp': {}, 'S': {}}

    sk_dumped = json.loads(sk_dumped)  # ecco questo è il 'load' fatto dopo. Verrà tolto ovviamente
    d = sk_dumped['D']
    d = d.encode('utf-8')
    d = groupObj.deserialize(d)
    Dict1['D'] = d

    dj = sk_dumped['Dj']
    for u in dj:
        s = dj[u].encode('utf-8')
        s = groupObj.deserialize(s)
        Dict1['Dj'][u] = s

    djp = sk_dumped['Djp']
    for u in djp:
        s = djp[u].encode('utf-8')
        s = groupObj.deserialize(s)
        Dict1['Djp'][u] = s

    Dict1['S'] = sk_dumped['S']

    return Dict1


def key_encoder(sk):
    Dict = {'D': None, 'Dj': {}, 'Djp': {}, 'S': {}}

    d = sk['D']
    d = groupObj.serialize(d)
    d = d.decode('utf-8')
    Dict['D'] = d

    dj = sk['Dj']
    for u in dj:
        s = groupObj.serialize(dj[u])
        s = s.decode('utf-8')
        Dict['Dj'][u] = s

    djp = sk['Djp']
    for u in djp:
        s = groupObj.serialize(djp[u])
        s = s.decode('utf-8')
        Dict['Djp'][u] = s

    Dict['S'] = sk['S']

    return Dict


def key_decoder(sk_dumped):
    Dict1 = {'D': None, 'Dj': {}, 'Djp': {}, 'S': {}}

    sk_dumped = json.loads(sk_dumped)
    sk_dumped = ast.literal_eval(sk_dumped)
    d = sk_dumped['D']
    d = d.encode('utf-8')
    d = groupObj.deserialize(d)
    Dict1['D'] = d

    dj = sk_dumped['Dj']
    for u in dj:
        s = dj[u].encode('utf-8')
        s = groupObj.deserialize(s)
        Dict1['Dj'][u] = s

    djp = sk_dumped['Djp']
    for u in djp:
        s = djp[u].encode('utf-8')
        s = groupObj.deserialize(s)
        Dict1['Djp'][u] = s

    Dict1['S'] = sk_dumped['S']

    return Dict1
