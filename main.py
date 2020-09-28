from connection import Server_config
import asyncio

class Diy_http_server:
    def __init__(self):
        asyncio.run(Server_config('127.0.0.1', 5525).listening())

if __name__ == '__main__':
    Diy_http_server()