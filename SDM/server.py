import socket
import ssl
import threading
import abenc_adapt_hybrid
from datetime import datetime
import random
import sqlite3
from hashlib import sha512

HEADER = 64
PORT = 5052
server_cert = 'Keys/server.crt'
server_key = 'Keys/server.key'
client_certs = 'Keys/client.crt'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

"""
creation and connection of the secure channel using SSL protocol
"""
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)
bindsocket = socket.socket()
bindsocket.bind(ADDR)
bindsocket.listen(5)

"""
function triggered by the client handler. Here starts the ciphering of the message with the policy.
"""


def create(message):
    abenc_adapt_hybrid.main(message[1], message[2], message[3])


"""
function that handles the requests from the clients. There is only one request possible, namely the 
ciphering of a message with a policy.
"""


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            # print(f"[{addr}] {msg}")
            conn.send("Msg received!".encode(FORMAT))
            message = msg.split('||')
            if message[0] == "Please certify signature":
                now = datetime.now()
                now = int(now.strftime("%Y%m%d%H%M%S%f"))
                random.seed(now)
                number_to_sign = random.randint(1, 2 ** 64)
                connection = sqlite3.connect('Database_SDM/signatures.db')
                x = connection.cursor()
                x.execute("INSERT OR IGNORE INTO signatures VALUES (?,?)",
                          (message[1], str(number_to_sign)))
                connection.commit()
                conn.send(b'Ecco qui il numero: ' + str(number_to_sign).encode())
            if message[0] == "Please cipher this message":
                connection = sqlite3.connect('Database_SDM/signatures.db')
                x = connection.cursor()
                x.execute("SELECT * FROM signatures WHERE address = ? ORDER BY number DESC LIMIT 1;", (message[3],))
                user_signature = x.fetchall()
                user_signature = user_signature[0][1]
                connection1 = sqlite3.connect('Database_Reader/public_key.db')
                y = connection1.cursor()
                y.execute("SELECT * FROM publicKeys WHERE address = ?", (message[3],))
                user_public_key = y.fetchall()
                hash = int.from_bytes(sha512(str(user_signature).encode()).digest(), byteorder='big')
                hashFromSignature = pow(int(message[4]), int(user_public_key[0][2]), int(user_public_key[0][1]))
                if hash == hashFromSignature:
                    create(message)

    conn.close()


"""
main function starting the server. It listens on a port and waits for a request from a client
"""


def start():
    bindsocket.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        newsocket, fromaddr = bindsocket.accept()
        conn = context.wrap_socket(newsocket, server_side=True)
        thread = threading.Thread(target=handle_client, args=(conn, fromaddr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
