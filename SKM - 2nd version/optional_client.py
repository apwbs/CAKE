import socket
import ssl

HEADER = 64
PORT = 5051
FORMAT = 'utf-8'
server_sni_hostname = 'example.com'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.17.0.2"
ADDR = (SERVER, PORT)
server_cert = 'Keys/server.crt'
client_cert = 'Keys/client.crt'
client_key = 'Keys/client.key'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)
    # print(conn.recv(6000).decode(FORMAT))
    a = conn.recv(6000).decode(FORMAT)
    if 'Ecco qui la key caro client: ' in a:
        print(a[29:])
        with open("key_" + sender + ".txt", "w") as text_file:
            text_file.write(a[29:])
    else:
        print(a)


sender = '0x22'
# send("Please generate my key//" + sender)

sender_key = open("key_" + sender + ".txt", 'r')
with open("key_" + sender + ".txt") as f:
    sender_key = f.readlines()
sender_key = sender_key[0]
send("Please read my data//" + sender + "//" + sender_key)

send(DISCONNECT_MESSAGE)
