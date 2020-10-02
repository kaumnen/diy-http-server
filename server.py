import asyncio
from configparser import ConfigParser


# read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# get the data
server_info = config_object["SERVERCONFIG"]

server_address = server_info["host"]
server_port = server_info["port"]

print(f'Listening on {server_address}:{server_port}')

# function for sending a message to client
async def writing_to_client(sender, message):
    sender.write(message.encode())
    await sender.drain()


# function that handles connection with a client
async def handle_echo(reader, writer):

    await writing_to_client(writer, 'Welcome to the server!\n\n'
                                    'Send \'HELP\' to get list of available commands!\n\n')

    addr = writer.get_extra_info('peername')
    print(f'[*] Connected to {addr}!')

    # dictionary which holds simple word:definition pairs
    protocol_beta = {'word': 'definition'}

    # with connection on, function accordingly
    while True:
        await writing_to_client(writer, '>>% ')

        # receiving messages from client
        data = await reader.read(10000)
        message = data.decode()

        print(f'Received {message} from {addr}')

        # GET method
        if 'GET' in message:
            if len(message.split()) == 2:
                try:
                    await writing_to_client(writer, f'\nDEFINITION - {str(protocol_beta[message.split()[1]])}\n\n')

                except KeyError:
                    await writing_to_client(writer, f'\nERROR - word \'{message.split()[1]}\' is not defined!\n\n')

        # SET method
        elif 'SET' in message:
            # this checks if user provided correct pattern
            if len(message.split()) < 3:
                await writing_to_client(writer, 'Error! Type HELP for more information.\n')

            else:
                # splitting message and making new key:value pair for a dictionary
                new_combo = message.split()
                protocol_beta[new_combo[1]] = ' '.join(new_combo[2:])

                await writing_to_client(writer, '\nFinishing..\n')
                await asyncio.sleep(2)

                await writing_to_client(writer, 'Added following definition:\n')
                await writing_to_client(writer, '\n#####\n')
                await writing_to_client(writer, f'# {new_combo[1]}: {protocol_beta[new_combo[1]]}')
                await writing_to_client(writer, '\n#####\n')

        # ALL method / displaying all words and their definitions
        elif 'ALL' in message:
            await writing_to_client(writer, 'These are all defined words:\n')
            await writing_to_client(writer, '\n#####\n# ')

            # going through dictionary keys and printing them to client
            for i in protocol_beta.keys():
                await writing_to_client(writer, i + '  ')
            await writing_to_client(writer, '\n#####\n\n')

        # CLEAR method / clears all words and their definitions
        elif 'CLEAR' in message:
            await writing_to_client(writer, '\nClearing all definitions. Please wait...\n')

            await asyncio.sleep(2)
            # wiping dictionary
            protocol_beta.clear()
            await writing_to_client(writer, 'All definitions are deleted now.\n\n')

        # HELP method / displays all available commands
        elif 'HELP' in message:
            await writing_to_client(writer, 'These are all commands you can use, make sure to CAPITALISE:\n')
            await writing_to_client(writer, '\n#####\n')
            await writing_to_client(writer,
                                    '# GET - Get definition of word\n# SET - Set a definition for new word\n'
                                    '# CLEAR - Clear all definitions\n# ALL - List all definitions\n'
                                    '# HELP - View all available commands\n# EXIT - You guessed it :)'
                                    )
            await writing_to_client(writer, '\n#####\n\n')

        # EXIT method / terminating connection
        elif 'EXIT' in message:
            await writing_to_client(writer, 'Sending connection closing order. Please wait...')
            await asyncio.sleep(2)
            print(f'[*] Disconnected from {addr}!')
            # closing connection to client
            break

    writer.close()


async def main():
    # starting server
    server = await asyncio.start_server(handle_echo, str(server_address), server_port)

    # keeping server alive over and over again
    async with server:
        await server.serve_forever()


# run program
asyncio.run(main())
