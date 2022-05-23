import socket
import ssl
import random
from datetime import datetime

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
server_sni_hostname = 'example.com'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.17.0.2"
ADDR = (SERVER, PORT)
server_cert = 'Keys/server.crt'
client_cert = 'Keys/client.crt'
client_key = 'Keys/client.key'

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
    print(conn.recv(msg_length).decode(FORMAT))


# policy = '((four or three) and (two or one))'
text = 'Manufacturer_company: Beta\nAddress: 82, Beta street\nE-mail: manufacturer.beta@mail.com\n' \
       'Frames_quantity: 8\nPropeller: 80\nPropeller_Guard: 63\nCamera: 30\nController_quantity: 4\n' \
       'Amount_payed: 12000$//' \
       'Manufacturer_company: Beta\nAddress: 82, Beta street\nE-mail: manufacturer.beta@mail.com\n' \
       'IMU_quantity: 6\nESC_quantity: 40\nEngines_quantity: 9\nBatteries_quantity: 25\nAmount_payed: 9850$//' \
       'Ciao ciao ciao ciao'
policy = '(16 and 86)//(4 or 77)//52'
sender = '0x989ab0A74915727f4e9dd7057EE7db71bA3DFeaD'
# text = 'ciao Marzia!'
# policy = '10'
now = datetime.now()
now = int(now.strftime("%Y%m%d%H%M%S%f"))
random.seed(now)
message_id_1 = random.randint(1, 2 ** 64)
message_id_2 = random.randint(1, 2 ** 64)
message_id_3 = random.randint(1, 2 ** 64)
message_ids = str(message_id_1) + '//' + str(message_id_2) + '//' + str(message_id_3)
send("Please cipher this message||" + text + "||" + policy + "||" + message_ids + "||" + sender)
# send("Please cipher this message||" + text + "||" + policy + "||" + str(message_id_1))
# exit()
input()
send("Hello Everyone!")
input()
send("Hello Tim!")

send(DISCONNECT_MESSAGE)
