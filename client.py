import sys
import os
import socket
import select

class Client:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.1.102"
    port = 8025

    def __init__(self):
        self.client_list = []
        self.getHostAndPort()
        self.connectServer()


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
    def connectServer(cls):
        try:
            cls.server.connect((cls.host, cls.port))
        except socket.error as e:
            print(e)


    def run(self):
        while True:
            sockets_list = [sys.stdin, self.server]
            read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])

            for socks in read_sockets:
                if socks == self.server:
                    message = socks.recv(4096)
                else:
                    message = sys.stdin.readline()
                    self.server.send(str.encode(message))
                    sys.stdout.write("<You>")
                    sys.stdout.write(message)
                    sys.stdout.flush()
            
            
def main():
    c = Client()
    c.run()
        

if __name__ == "__main__":
    main()