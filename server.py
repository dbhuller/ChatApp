"""Server for multithreaded chat application"""
import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 12000
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}
addresses = {}

def accept_new_connections():
    """Handles accept() for incomming client connections"""
    while True:
        client, client_address = server.accept()
        print("%s:%s has connected" % client_address)
        client.send(bytes("Connected Successfully! Enter your name and press enter!", "utf8"))
        addresses[client] = client_address
        #Create new thread

def handle_client(client):
    """Handles single client connection"""
    name = client.recv(BUFFER_SIZE).decode("utf8")
    welcome_msg = "Welcome %s! type {quit} to exit." % name
    client.send(bytes(welcome_msg, "utf8"))
    msg = "%s has joined the chat!" % name
    # Broadcast mesg to cleints
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFFER_SIZE)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat" % name, "utf8"))
            break

def broadcast(msg, prefix=""):
    """boradcasts a message to all connected clients"""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


if __name__ == "__main__":
    server.listen(5)
    print("Waiting for Connections on <%s/%d>" % (HOST, PORT))
    ACCEPT_THREAD = Thread(target=accept_new_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()
