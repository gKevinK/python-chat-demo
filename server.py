#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket
import threading

HOST = "0.0.0.0"
PORT = 12345

Clients = []

class Client:
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.name = sock.recv(1024).decode('utf-8')

    def get_name(self):
        return self.name + str(self.addr)

    def exit(self):
        self.sock.close()

def recv_thread(client):
    while True:
        data = client.sock.recv(1024)
        message = data.decode('utf-8')
        if message == "exit":
            print("[Exit]" + client.get_name() + "exit.")
            Clients.remove(client)
            break
        print(client.get_name() + ": " + message)
        broadcast(client.get_name() + ": " + message)

def broadcast(mesg):
    for client in Clients:
        client.sock.sendall(mesg.encode('utf-8'))

def main():
    print("Starting...")
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((HOST, PORT))
    ss.listen(5)
    print("Listening port: " + str(PORT))
    while True:
        conn, addr = ss.accept()
        client = Client(conn, addr)
        Clients.append(client)
        print("[Connect] " + client.get_name() + " connected.")
        threading.Thread(target=recv_thread, args=(client,)).start()
    ss.close()

if __name__ == "__main__":
    main()
