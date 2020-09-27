import socket
import unittest as ut
import time

class Test_responses(ut.TestCase):

    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 5525))

    def tearDown(self):
        self.s.send('EXIT'.encode('utf-8'))

    def testGET(self):
        self.s.recv(1024)
        self.s.send('GET word'.encode('utf-8'))
        self.s.recv(1024)
        self.assertEqual(self.s.recv(4096).decode().strip(), 'DEFINITION - definition')

if __name__ == '__main__':
    ut.main()