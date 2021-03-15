import socket
from snake import *
from _thread import *
import pickle
import sys

server = "192.168.2.177"
port = 42069
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server started")

players = ["eric"]

def threaded_client(conn,):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)
            conn.sendall(str.encode(reply))
        except:
            break

        print("Lost Connection")
        conn.close()




board = Board()
start_new_thread(Board.startgame, (board,))

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))