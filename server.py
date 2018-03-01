import sys
import os
import socket
import re
from threading import Thread
import requests


class Server:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host =  "192.168.1.102"
    port = 8037

    def __init__(self):
        print(self.host)
        self.client_list = []
        self.getHostAndPort()
        self.setServer()

    @classmethod
    def getHostAndPort(cls):
        if len(sys.argv) > 2:
            cls.host = sys.argv[1]
            try:
                cls.port = int(sys.argv[2])
            except ValueError:
                print("Must be decimal")
        else:
            print("Using default server host as {} and port as {}".format(cls.host, str(cls.port)))
    
    @classmethod
    def setServer(cls):
        try:
            cls.server.bind((cls.host, cls.port))
        except socket.error as e:
            print(e)
        cls.server.listen(5)

    def run(self):
        while True:
            conn, addr = self.server.accept()
            self.client_list.append(conn)
            t = Thread(target = self.clientThread, args = (conn, addr))
            print(t, "new Connection Found")
            t.start()

    def clientThread(self, conn, addr):
        while True:
            try:
                message = conn.recv(4096)
                if message:
                    print_msg = "<" + addr[0] + "> " + message.decode("utf-8")
                    print(print_msg)
                    self.broadcast(message, conn)

            except socket.error as e:
                print("exception in message", e)


    def broadcast(self, message, connection):
        for client in self.client_list:          
            if client!=connection:
                try:
                    client.send(message)
                except socket.error as e:
                     print("Client closed with exception: {}".format(e))
                     client.close()    
                     self.removeClient(client)

    def removeClient(self, conn):
        if conn in self.client_list:
            self.client_list.remove(conn)

def main(): # driver function
    s = Server()
    s.run()

if __name__ == "__main__":
    main()
