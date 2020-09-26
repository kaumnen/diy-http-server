import socket
import time

HOST = '127.0.0.1'
PORT = 5525

protocol_beta = {'word':'definition'}

#setting socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    client_socket, address = s.accept()

    #when connection is open
    with client_socket:
        print(f'Connection from {address} has been established!')
        client_socket.send('Welcome to the server!\n\nSend \'ALL\' to get list of available commands!\n\n'.encode('ascii'))
        while True:

            client_socket.send('>>% '.encode('ascii'))
            reply = client_socket.recv(1024).decode().strip()

            #making of simple protocol
        
            if 'GET' in reply:
                if len(reply.split()) == 2:
                    try:
                        client_socket.send(f'ANSWER - {str(protocol_beta[reply.split()[1]])}\n'.encode('utf-8'))
                    except KeyError:
                        client_socket.send(f'ERROR - word \'{reply.split()[1]}\' is not defined!\n'.encode('utf-8'))
                    

            elif 'SET' in reply:

                if len(reply.split()) < 3:
                    client_socket.send('Error! Type HELP for more information.\n'.encode('utf-8'))
                else:    
                    new_combo = reply.split()
                    protocol_beta[new_combo[1]] = new_combo[2:]
                    
                    client_socket.send('Finishing..\n'.encode('utf-8'))
                    time.sleep(2)

                    client_socket.send('\n##########################\n'.encode('utf-8'))
                    client_socket.send(f'Added following word:definition combo:\n\n{new_combo[1]}:{protocol_beta[new_combo[1]]}'.encode('utf-8'))
                    client_socket.send('\n##########################\n'.encode('utf-8'))

                    client_socket.send('\nYou can use \'ALL\' in request to print all available words,\nor \'CLEAR\' to, you guessed it, clear all created words.\n'.encode('utf-8'))
            
            #elif reply == "CLEAR":

            elif reply == "ALL":
                client_socket.send('These are all commands you can use / make sure to CAPITALISE:\n'.encode('utf-8'))

                client_socket.send('\n##########################\n'.encode('utf-8'))
                client_socket.send('GET, SET, CLEAR, ALL, EXIT'.encode('utf-8'))
                client_socket.send('\n##########################\n\n'.encode('utf-8'))

            elif reply == 'EXIT':
                client_socket.send('Closing connection. Please wait...'.encode('utf-8'))
                time.sleep(2)
                break

        client_socket.close()