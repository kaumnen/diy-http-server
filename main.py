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
        client_socket.send('Welcome to the server!\n\nSend \'HELP\' to get list of available commands!\n\n'.encode('ascii'))
        while True:

            client_socket.send('>>% '.encode('ascii'))
            reply = client_socket.recv(1024).decode().strip()

            #making of simple protocol
        
            if 'GET' in reply:
                if len(reply.split()) == 2:
                    try:
                        client_socket.send(f'\nDEFINITION - {str(protocol_beta[reply.split()[1]])}\n\n'.encode('utf-8'))
                    except KeyError:
                        client_socket.send(f'\nERROR - word \'{reply.split()[1]}\' is not defined!\n\n'.encode('utf-8'))
                    

            elif 'SET' in reply:

                if len(reply.split()) < 3:
                    client_socket.send('Error! Type HELP for more information.\n'.encode('utf-8'))
                else:    
                    new_combo = reply.split()
                    protocol_beta[new_combo[1]] = ' '.join(new_combo[2:])
                    
                    client_socket.send('\nFinishing..\n'.encode('utf-8'))
                    time.sleep(2)

                    client_socket.send('Added following definition:\n'.encode('utf-8'))

                    client_socket.send('\n#####\n'.encode('utf-8'))
                    client_socket.send(f'# {new_combo[1]}: {protocol_beta[new_combo[1]]}'.encode('utf-8'))
                    client_socket.send('\n#####\n'.encode('utf-8'))

            
            elif reply == "CLEAR":
                client_socket.send('\nClearing all definitions. Please wait...\n'.encode('utf-8'))
                time.sleep(2)
                protocol_beta.clear()
                client_socket.send('All definitions are deleted now.\n\n'.encode('utf-8'))


            elif reply == "ALL":
                client_socket.send('These are all defined words:\n'.encode('utf-8'))
                client_socket.send('\n#####\n# '.encode('utf-8'))
                
                for i in protocol_beta.keys():
                    client_socket.send(i.encode('utf-8'))
                
                client_socket.send('\n#####\n\n'.encode('utf-8'))

                
            elif reply == 'HELP':
                client_socket.send('These are all commands you can use, make sure to CAPITALISE:\n'.encode('utf-8'))

                client_socket.send('\n#####\n'.encode('utf-8'))
                client_socket.send('# GET - Get definition of word\n# SET - Set a definition for new word\n# CLEAR - Clear all definitions\n# ALL - List all defitinions\n# HELP - View all available commands\n# EXIT - You guessed it :)'.encode('utf-8'))
                client_socket.send('\n#####\n\n'.encode('utf-8'))


            elif reply == 'EXIT':
                client_socket.send('Sending connection closing order. Please wait...'.encode('utf-8'))
                time.sleep(2)
                break

        client_socket.close()