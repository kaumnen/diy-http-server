import socket
import time
from server import Server_operations
from config import Server_config

http_server_config = Server_config('127.0.0.1', 5525)

#until connection is established
while not http_server_config.connection_established:
    http_server_ops = http_server_config.listening()

while not http_server_ops.shutdown:
    http_server_ops.maintaining_connection()

    if 'GET' in http_server_ops.reply:
        http_server_ops.get_definition()

    elif 'SET' in http_server_ops.reply:
        http_server_ops.set_definition()

    elif http_server_ops.reply == 'ALL':
        http_server_ops.display_definitions()

    elif http_server_ops.reply == 'CLEAR':
        http_server_ops.clear_definitions()

    elif http_server_ops.reply == 'HELP':
        http_server_ops.display_help()
    
    elif http_server_ops.reply == 'EXIT':
        http_server_ops.terminate_connection()

    elif http_server_ops.shutdown:
        http_server_ops.terminate_connection()
        break