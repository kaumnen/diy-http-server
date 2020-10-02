import asyncio
import logging

print('Listening on 127.0.0.1:8888')

# function for sending a message to client
async def writing_to_client(sender, message):
    sender.write(message.encode())
    await sender.drain()


# function that handles connection with a client
async def handle_echo(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f'[*] Connected to {addr}!')
    shutdown = False

    #make log file
    logging.basicConfig(filename='communication.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # list of all methods used in HTTP request
    METHODS = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']

    # with connection on, function accordingly
    while True:

        data = await reader.read(10000)
        message = data.decode()

        http_request_lines = message.split('\r\n')
        request = [x.split(' ') for x in http_request_lines]
        USUALL_HEADERS = ['Host:', 'Connection:', 'User-Agent:', 'Accept:']
        # if statements to decide how to respond
        # HTTP request
        if request[0][0] in METHODS:

            # retrieve http first header
            method = request[0][0]
            resource = request[0][1]
            http_version = request[0][2]

            # retrieve all other http headers in dictionary form
            HEADERS = {}
            for i in request[1:]:
                if i:
                    key = i[0]
                    value = ' '.join(i[1:])

                    HEADERS[key] = value

            # checking if header is valid by ensuring that all of usual headers are present in request
            for j in USUALL_HEADERS:

                if j not in HEADERS.keys():
                    await writing_to_client(writer,
                                            f'{http_version} 400 Bad Request \r\n\r\nI\'m sorry, I don\'t understand!')
                    logging.error(f'[ j ] - Header not found! Bad request - 400.')
                    shutdown = True
                    break

            if shutdown:
                break

            # response to client
            try:
                with open('www/' + resource[1:]) as text:
                    file_text = text.readline()

                    await writing_to_client(writer, f'{http_version} 200 OK \r\n\r\n{file_text}')
                    break

            # if file doesnt exist
            except IOError as e:
                await writing_to_client(writer, f'{http_version} 404 Not Found \r\n\r\nError! We don\'t have that file!')

            finally:
                break


        else:
            # if server receives invalid method, log error in file
            logging.error(f'[ {message.split()[0]} ] - Invalid method detected!')
            break

    print(f'\n[*] Disconnected from {addr}!\n')
    writer.close()


async def main():
    # starting server
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)

    # keeping server alive over and over again
    async with server:
        await server.serve_forever()


# run program
asyncio.run(main())
