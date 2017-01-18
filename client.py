#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket, threading

HOST = "127.0.0.1"
PORT = 12345

global s

def recv_thread():
    try:
        while True:
            data = s.recv(1024)
            if not data:
                break
            mesg = data.decode('utf-8')
            print(mesg)
    except ConnectionAbortedError:
        pass

def main():
    global s
    name = input("Input your name: ")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected to " + HOST + ", port " + str(PORT))
    except Exception:
        print("Failed to connect, exiting.")
        exit()

    t = threading.Thread(target=recv_thread)
    t.start()
    s.sendall(name.encode('utf-8'))
    while True:
        data = input()
        s.sendall(data.encode('utf-8'))
        if data == "exit":
            break     
    s.close()

if __name__ == "__main__":
    main()
