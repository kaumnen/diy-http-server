import unittest as ut
import requests as rq
from server import Server_operations
from config import Server_config


http_server_config = Server_config('127.0.0.1', 5525)
while not http_server_config.connection_established:
    http_server_ops = http_server_config.listening()

class testResponses(ut.TestCase):
    def GETtest(self):
        
        test = [http_server_config.client_socket]
        self.assertEqual()



#still to be finished