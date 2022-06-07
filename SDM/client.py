import socket
import ssl
from hashlib import sha512
import sqlite3

HEADER = 64
PORT = 5052
FORMAT = 'utf-8'
server_sni_hostname = 'example.com'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.17.0.2"
ADDR = (SERVER, PORT)
server_cert = 'Keys/server.crt'
client_cert = 'Keys/client.crt'
client_key = 'Keys/client.key'

# Connection to SQLite3 public_Keys
connection = sqlite3.connect('Database_Reader/private_key.db')
y = connection.cursor()

"""
creation and connection of the secure channel using SSL protocol
"""

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect(ADDR)

"""
function to handle the sending and receiving messages.
"""


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    print(send_length)
    conn.send(message)
    receive = conn.recv(6000).decode(FORMAT)
    print(receive)


# policy = '((four or three) and (two or one))'
text = 'Manufacturer_company: Beta \n Address: 82 , Beta street \n Email: mnfctr . beta@mail . com//asdasdasd'
policy = '(1621 and 862341)//asdasduoad'
sender = '0x989ab0A74915727f4e9dd7057EE7db71bA3DFeaD'

# send("Please certify signature||" + sender)

msg = b'9679842212974955389'
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
y.execute("SELECT * FROM privateKeys WHERE address = ?", (sender,))
user_privateKey = y.fetchall()
signature = pow(hash, int(user_privateKey[0][2]), int(user_privateKey[0][1]))
# input()
# input()
send("Please cipher this message||" + text + "||" + policy + "||" + sender + "||" + str(signature))
# exit()
# input()
# send("Hello Everyone!")
# input()
# send("Hello Tim!")

# send(DISCONNECT_MESSAGE)
