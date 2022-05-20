import hashlib

a = 'Company_name: Alpha\nAddress: 34, Alpha street\nE-mail:company.alpha@mail.com\nQuantity:5\nAmount_payed:5000$'
b = 16184025537323209064
s_1 = a + str(b)
s_1 = s_1.encode()
s_1_hashed = hashlib.sha256(s_1)
hex_dig = s_1_hashed.hexdigest()
print(hex_dig)
