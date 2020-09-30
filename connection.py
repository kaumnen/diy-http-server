import socket
import asyncio
from server import Server_operations


class Server_config:

    def __init__(self, HOST, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))

    # listening as long as there is not a connection
    async def listening(self, n_of_connections = 1):
        # listen for connection
        self.s.listen(n_of_connections)

        while True:
            client_socket, address = self.s.accept()

            # when connection happens, returns server object, who is initialised with client_socket and address object

            asyncio.create_task(Server_operations(client_socket, address).communication())
