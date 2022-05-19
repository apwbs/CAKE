import socket
import ssl

HEADER = 64
PORT = 5053
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
    conn.send(message)
    receive = conn.recv(6000).decode(FORMAT)
    print(receive)


case_id = '8897945712264932062'
message_id = '8654962570407031192'
requester = '0xC869a3B0Aed8121c95d2F0016E7F4bBe2a5B9754'
sender = '0x989ab0A74915727f4e9dd7057EE7db71bA3DFeaD'
# send("Please generate my key//" + case_id + '//' + requester)
send("Please read my data//" + requester + '//' + case_id + '//' + message_id + '//' + sender)
# exit()
# poi voglio più message_id non solo uno

send(DISCONNECT_MESSAGE)
