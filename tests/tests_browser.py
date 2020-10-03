import unittest as ut
import requests
from configparser import ConfigParser

# read config.ini file
config_object = ConfigParser()
config_object.read("../config/config.ini")

# get the data
server_info = config_object["SERVERCONFIG_BROWSER"]

server_address = server_info["host"]
server_port = server_info["port"]


class Test_responses(ut.TestCase):

    # test for OK request
    def test_get_request(self):
        r = requests.get(f'http://{server_address}:{int(server_port)}/test.txt')
        self.assertEqual(200, r.status_code)

    # test for NOT FOUND request
    def test_not_found(self):
        r = requests.get(f'http://{server_address}:{int(server_port)}/foofoo')
        self.assertEqual(404, r.status_code)

    # security test
    def test_sec(self):
        r = requests.get(f'http://{server_address}:{int(server_port)}/../README.md')
        self.assertEqual(404, r.status_code)


if __name__ == '__main__':
    ut.main()
