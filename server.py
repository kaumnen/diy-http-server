import asyncio


class Server_operations:

    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.protocol_beta = {'word': 'definition'}
        print(f'Connection from {address} has been established!')
        self.shutdown = False

    async def messenger(self, message):
        self.client_socket.send(message.encode())

    def decoder(self):
        return self.client_socket.recv(1024).decode().strip()

    async def communication(self):
        await self.messenger('Welcome to the server!\n\nSend \'HELP\' to get list of available commands!\n\n')

        while not self.shutdown:
            await self.messenger('>>% ')
            self.reply = self.decoder()

            # GET method
            if 'GET' in self.reply:
                if len(self.reply.split()) == 2:
                    try:
                        await self.messenger(f'\nDEFINITION - {str(self.protocol_beta[self.reply.split()[1]])}\n\n')
                    except KeyError:
                        await self.messenger(f'\nERROR - word \'{self.reply.split()[1]}\' is not defined!\n\n')

            # SET method
            elif 'SET' in self.reply:
                if len(self.reply.split()) < 3:
                    await self.messenger('Error! Type HELP for more information.\n')
                else:
                    new_combo = self.reply.split()
                    self.protocol_beta[new_combo[1]] = ' '.join(new_combo[2:])

                    await self.messenger('\nFinishing..\n')
                    await asyncio.sleep(2)

                    await self.messenger('Added following definition:\n')

                    await self.messenger('\n#####\n')
                    await self.messenger(f'# {new_combo[1]}: {self.protocol_beta[new_combo[1]]}')
                    await self.messenger('\n#####\n')

            # ALL method / displaying all words and their definitions
            elif self.reply == 'ALL':
                await self.messenger('These are all defined words:\n')
                await self.messenger('\n#####\n# ')

                for i in self.protocol_beta.keys():
                    await self.messenger(i)

                await self.messenger('\n#####\n\n')

            # CLEAR method / clears all words and their definitions
            elif self.reply == 'CLEAR':
                await self.messenger('\nClearing all definitions. Please wait...\n')
                await asyncio.sleep(2)
                self.protocol_beta.clear()
                await self.messenger('All definitions are deleted now.\n\n')

            # HELP method / displays all available commands
            elif self.reply == 'HELP':
                await self.messenger('These are all commands you can use, make sure to CAPITALISE:\n')

                await self.messenger('\n#####\n')
                await self.messenger(
                    '# GET - Get definition of word\n# SET - Set a definition for new word\n'
                    '# CLEAR - Clear all definitions\n# ALL - List all definitions\n'
                    '# HELP - View all available commands\n# EXIT - You guessed it :)'
                                    )
                await self.messenger('\n#####\n\n')

            # EXIT method / terminating connection
            elif self.reply == 'EXIT':
                await self.messenger('Sending connection closing order. Please wait...')
                self.shutdown = True
                await asyncio.sleep(2)
                self.client_socket.close()
