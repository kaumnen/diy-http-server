import socket
import time

class Server_operations:

    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.protocol_beta = {'word':'definition'}
        self.shutdown = False

    #maintaining connection as long as signal for terminating connection is not received
    def maintaining_connection(self):
        if not self.shutdown:
            self.client_socket.send('>>% '.encode('ascii'))
            self.reply = self.client_socket.recv(1024).decode().strip()
        else:
            self.send_message_to_client('\n\nConnection closed. Thank you for your time! :)\n\n')

    #GET method
    def get_definition(self):
        if len(self.reply.split()) == 2:
                try:
                    self.client_socket.send(f'\nDEFINITION - {str(self.protocol_beta[self.reply.split()[1]])}\n\n'.encode('utf-8'))
                except KeyError:
                    self.client_socket.send(f'\nERROR - word \'{self.reply.split()[1]}\' is not defined!\n\n'.encode('utf-8'))
    
    #SET method
    def set_definition(self):
        if len(self.reply.split()) < 3:
            self.client_socket.send('Error! Type HELP for more information.\n'.encode('utf-8'))
        else:    
            new_combo = reply.split()
            self.protocol_beta[new_combo[1]] = ' '.join(new_combo[2:])
            
            self.client_socket.send('\nFinishing..\n'.encode('utf-8'))
            time.sleep(2)

            self.client_socket.send('Added following definition:\n'.encode('utf-8'))

            self.client_socket.send('\n#####\n'.encode('utf-8'))
            self.client_socket.send(f'# {new_combo[1]}: {protocol_beta[new_combo[1]]}'.encode('utf-8'))
            self.client_socket.send('\n#####\n'.encode('utf-8'))
    
    #ALL method / displaying all words and their definitions
    def display_definitions(self):
        self.client_socket.send('These are all defined words:\n'.encode('utf-8'))
        self.client_socket.send('\n#####\n# '.encode('utf-8'))
        
        for i in self.protocol_beta.keys():
            self.client_socket.send(i.encode('utf-8'))
        
        self.client_socket.send('\n#####\n\n'.encode('utf-8'))

    #CLEAR method / clears all words and their definitions
    def clear_definitions(self):
        self.client_socket.send('\nClearing all definitions. Please wait...\n'.encode('utf-8'))
        time.sleep(2)
        self.protocol_beta.clear()
        self.client_socket.send('All definitions are deleted now.\n\n'.encode('utf-8'))

    #HELP method / displays all available commands
    def display_help(self):
        self.client_socket.send('These are all commands you can use, make sure to CAPITALISE:\n'.encode('utf-8'))

        self.client_socket.send('\n#####\n'.encode('utf-8'))
        self.client_socket.send('# GET - Get definition of word\n# SET - Set a definition for new word\n# CLEAR - Clear all definitions\n# ALL - List all defitinions\n# HELP - View all available commands\n# EXIT - You guessed it :)'.encode('utf-8'))
        self.client_socket.send('\n#####\n\n'.encode('utf-8'))

    #EXIT method / terminating connection
    def terminate_connection(self):
        self.client_socket.send('Sending connection closing order. Please wait...'.encode('utf-8'))
        time.sleep(2)

        self.client_socket.close()