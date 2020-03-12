"""Tkinter GUI chat client and client code"""

import socket
from threading import Thread
import tkinter

HOST = input("Enter ip address: ")
PORT = input("Enter a port number: ")

if not PORT:
    PORT = 12000
else:
    PORT = int(PORT)

BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)


def receive():
    """Handles receiving messages"""
    while True:
        try:
            msg = client_socket.recv(BUFFER_SIZE).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError: # If client leaves the chat
            break

def send(event=None):
    """Handles sending messages"""
    msg = msg_to_send.get()
    msg_to_send.set("") # clear input field for next message
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_close(event=None):
    """Called when window is closed"""
    msg_to_send.set("{quit}")
    send()

# tkinter GUI code
top = tkinter.Tk()
top.title("Chat App")

msg_frame = tkinter.Frame(top)
msg_to_send = tkinter.StringVar()               # Message to be sent
msg_to_send.set("Type Your Message Here...")
scroll_bar = tkinter.Scrollbar(msg_frame)       # Scroll through past messages

msg_list = tkinter.Listbox(msg_frame, height=15, width=50, yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
msg_frame.pack()

msg_entry = tkinter.Entry(top, textvariable=msg_to_send)
msg_entry.bind("<Enter>", send)
msg_entry.pack()

send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_close)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
