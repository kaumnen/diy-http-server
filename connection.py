import socket
import time
import asyncio
from server import Server_operations

class Server_config:

    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))

    #listening as long as there is not a connection
    async def listening(self, n_of_connections = 1):

        #listen for connection
        
        
        while True:
            self.client_socket, self.address = self.s.accept()
            self.s.listen(n_of_connections)

            #when connection happens, returns server object, who is initialised with client_socket object
            
            print(f'Connection from {self.address} has been established!')
            await asyncio.create_task(Server_operations(self.client_socket).communication())
            