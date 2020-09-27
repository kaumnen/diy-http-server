import socket
import unittest as ut

class Test_responses(ut.TestCase):

    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 5525))

    def tearDown(self):
        self.s.close()
    
    def testGET(self):
        
        self.s.send('GET word\n'.encode('utf-8'))
        recieve = self.s.recv(4096).decode().strip()
        self.assertEqual(receive, 'DEFINITION - definition')

    def testSET(self):
        
        self.s.send('SET new one two three\n'.encode('utf-8'))
        recieve = self.s.recv(4096).decode().strip()
        self.assertEqual(receive, 'Finishing..\nAdded following definition:\n\n#####\n# new: one two three\n#####')

    def testEXIT(self):
        
        self.s.send('EXIT'.encode('utf-8'))
        recieve = self.s.recv(4096).decode().strip()
        self.assertEqual(recieve, 'Sending connection closing order. Please wait...')

if __name__ == '__main__':
    ut.main()