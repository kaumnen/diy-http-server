import socket
import time
import asyncio
from server import Server_operations

class Server_config:

    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        self.connection_established = False

    #listening as long as there is not a connection
    async def listening(self, n_of_connections = 5):

        #listen for connection
        self.s.listen(n_of_connections)
        
        while True:
            self.client_socket, self.address = self.s.accept()

            #when connection happens, returns server object, who is initialised with client_socket object
            if self.client_socket:
                print(f'Connection from {self.address} has been established!')
                self.client_socket.send('Welcome to the server!\n\nSend \'HELP\' to get list of available commands!\n\n'.encode('ascii'))
                self.connection_established = True
                await asyncio.create_task(Server_operations(self.client_socket).maintaining_connection())