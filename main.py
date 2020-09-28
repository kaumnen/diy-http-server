import socket
import time
from connection import Server_config
import asyncio

asyncio.run(Server_config('127.0.0.1', 5525).listening())
