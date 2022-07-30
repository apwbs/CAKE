import json
import socket
import ssl
from hashlib import sha512
import sqlite3

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
server_sni_hostname = 'example.com'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.17.0.3"
ADDR = (SERVER, PORT)
server_cert = 'Keys/server.crt'
client_cert = 'Keys/client.crt'
client_key = 'Keys/client.key'

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
    conn.send(message)
    receive = conn.recv(6000).decode(FORMAT)
    print(receive)
    # with open("key_" + requester + "--messageid_" + message_id + ".txt", "w") as text_file:
    #     text_file.write(json.dumps(receive[75:]))


message_id = '10163413069310470956'
slice_id = '8057614612533497852'
requester = '0xA5dfE42d5BE39A3aE6c45ED7aBbCD77F8647D54B'

with open("key_" + requester + "--messageid_" + message_id + ".txt") as f:
    requester_key = f.readlines()
requester_key = requester_key[0]

# send("Please certify signature||" + requester)

msg = b'5793998545963035261'
hash = int.from_bytes(sha512(msg).digest(), byteorder='big')
y.execute("SELECT * FROM privateKeys WHERE address = ?", (requester,))
user_privateKey = y.fetchall()
signature = pow(hash, int(user_privateKey[0][2]), int(user_privateKey[0][1]))

# send("Please generate my key||" + message_id + '||' + requester + '||' + str(signature))
send("Please read my data||" + message_id + '||' + slice_id + '||' + requester_key + '||' + requester + '||' + str(signature))
# exit()
# poi voglio più message_id non solo uno

send(DISCONNECT_MESSAGE)
