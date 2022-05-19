import hashlib

a = 'Ciao Marzia!'
b = 9300620666546293951
s_1 = a + str(b)
s_1 = s_1.encode()
s_1_hashed = hashlib.sha256(s_1)
hex_dig = s_1_hashed.hexdigest()
print(hex_dig)
