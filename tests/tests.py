import socket
import unittest as ut
from configparser import ConfigParser


# read config.ini file
config_object = ConfigParser()
config_object.read("../config/config.ini")

# get the data
server_info = config_object["SERVERCONFIG"]

server_address = server_info["host"]
server_port = server_info["port"]


class Test_responses(ut.TestCase):

    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_address, int(server_port)))

    def tearDown(self):
        self.s.send('EXIT'.encode('utf-8'))
        self.s.close()

    def testGET(self):
        self.s.recv(1024)
        self.s.send('GET word'.encode('utf-8'))
        self.s.recv(1024)
        self.assertEqual(self.s.recv(4096).decode().strip(), 'DEFINITION - definition')


if __name__ == '__main__':
    ut.main()
