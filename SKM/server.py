import socket
import ssl
import threading
import abenc_adapt_hybrid
import abenc_adapt_hybrid_reading

HEADER = 64
PORT = 5052
server_cert = 'Keys/server.crt'
server_key = 'Keys/server.key'
client_certs = 'Keys/client.crt'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

bindsocket = socket.socket()
bindsocket.bind(ADDR)
bindsocket.listen(5)


def generate(message):
    return abenc_adapt_hybrid.main(message)


def read(message):
    return abenc_adapt_hybrid_reading.main(message)


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

            print(f"[{addr}] {msg}")
            conn.send("Msg received!".encode(FORMAT))
            message = msg.split('//')
            if message[0] == "Please generate my key":
                response = generate(message)
                response = bytes(response, FORMAT)
                conn.send(b'Ecco qui il link di IPFS key caro client: ' + response)
            if message[0] == "Please read my data":
                response = read(message)
                print(response)
                conn.send(b'Ecco qui il testo e il salt caro client:\n\n' + response[0] + b'\n\n' + response[1])

    conn.close()


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
