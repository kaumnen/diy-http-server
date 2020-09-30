import asyncio

async def handle_echo(reader, writer):

    writer.write('Welcome to the server!\n\nSend \'HELP\' to get list of available commands!\n\n'.encode())
    await writer.drain()

    protocol_beta = {'word':'definition'}

    while True:
        writer.write('>>% '.encode())
        await writer.drain()
        data = await reader.read(100)
        message = data.decode()

        addr = writer.get_extra_info('peername')
        print(f'Received {message} from {addr}')

        # GET method
        if 'GET' in message:
            if len(message.split()) == 2:
                try:
                    writer.write(f'\nDEFINITION - {str(protocol_beta[message.split()[1]])}\n\n'.encode())
                    await writer.drain()
                except KeyError:
                    writer.write(f'\nERROR - word \'{message.split()[1]}\' is not defined!\n\n'.encode())
                    await writer.drain()

        # SET method
        elif 'SET' in message:
            if len(message.split()) < 3:
                writer.write('Error! Type HELP for more information.\n'.encode())
                await writer.drain()
            else:
                new_combo = message.split()
                protocol_beta[new_combo[1]] = ' '.join(new_combo[2:])

                writer.write('\nFinishing..\n'.encode())
                await writer.drain()
                await asyncio.sleep(2)

                writer.write('Added following definition:\n'.encode())
                await writer.drain()

                writer.write('\n#####\n'.encode())
                await writer.drain()
                writer.write(f'# {new_combo[1]}: {protocol_beta[new_combo[1]]}'.encode())
                await writer.drain()
                writer.write('\n#####\n'.encode())
                await writer.drain()

        # ALL method / displaying all words and their definitions
        elif 'ALL' in message:
            writer.write('These are all defined words:\n'.encode())
            await writer.drain()
            writer.write('\n#####\n# '.encode())
            await writer.drain()

            for i in protocol_beta.keys():
                writer.write(i.encode())
                await writer.drain()

            writer.write('\n#####\n\n'.encode())
            await writer.drain()

        # CLEAR method / clears all words and their definitions
        elif 'CLEAR' in message:
            writer.write('\nClearing all definitions. Please wait...\n'.encode())
            await writer.drain()
            await asyncio.sleep(2)
            protocol_beta.clear()
            writer.write('All definitions are deleted now.\n\n'.encode())
            await writer.drain()

        # HELP method / displays all available commands
        elif 'HELP' in message:
            writer.write('These are all commands you can use, make sure to CAPITALISE:\n'.encode())
            await writer.drain()

            writer.write('\n#####\n'.encode())
            await writer.drain()
            writer.write(
                '# GET - Get definition of word\n# SET - Set a definition for new word\n'
                '# CLEAR - Clear all definitions\n# ALL - List all definitions\n'
                '# HELP - View all available commands\n# EXIT - You guessed it :)'.encode()
                                )
            await writer.drain()
            writer.write('\n#####\n\n'.encode())
            await writer.drain()

        # EXIT method / terminating connection
        elif 'EXIT' in message:
            writer.write('Sending connection closing order. Please wait...'.encode())
            await writer.drain()
            shutdown = True
            await asyncio.sleep(2)
            writer.close()
            break

async def main():

    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

asyncio.run(main())
