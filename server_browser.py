import asyncio
import logging
from configparser import ConfigParser


# read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# get the data
server_info = config_object["SERVERCONFIG_BROWSER"]

server_address = server_info["host"]
server_port = server_info["port"]
server_web_directory = server_info["web_directory"]

print(f'Listening on {server_address}:{server_port}')

# function for sending a message to client
async def writing_to_client(sender, message):
    sender.write(message.encode())
    await sender.drain()


# function that handles connection with a client
async def handle_echo(reader, writer):

    addr = writer.get_extra_info('peername')
    print(f'[*] Connected to {addr}!')
    shutdown = False

    # make log file
    logging.basicConfig(filename='communication.log', filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # list of all methods used in HTTP request, and headers u can find in every http request from browser
    methods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']
    usual_headers = ['Host:', 'Connection:', 'User-Agent:', 'Accept:']

    # with connection on, function accordingly
    while True:

        data = await reader.read(10000)
        message = data.decode()

        http_request_lines = message.split('\r\n')
        request = [x.split(' ') for x in http_request_lines]

        # HTTP request
        if request[0][0] in methods:

            # retrieve http first header
            resource = request[0][1]
            http_version = request[0][2]

            # retrieve all other http headers in dictionary form
            headers = {}
            for i in request[1:]:
                if i:
                    key = i[0]
                    value = ' '.join(i[1:])

                    headers[key] = value

            # checking if header is valid by ensuring that all of usual headers are present in request
            for j in usual_headers:

                if j not in headers.keys():
                    await writing_to_client(writer,
                                            f'{http_version} 400 Bad Request \r\n\r\nI\'m sorry, I don\'t understand!')
                    logging.error(f'[ j ] - Header not found! Bad request - 400.')
                    shutdown = True
                    break

            if shutdown:
                break

            # response to client
            try:
                with open(server_web_directory+ resource[1:]) as text:
                    file_text = text.readline()

                    await writing_to_client(writer, f'{http_version} 200 OK \r\n\r\n{file_text}')
                    break

            # if file doesnt exist
            except IOError:
                await writing_to_client(writer,
                                        f'{http_version} 404 Not Found \r\n\r\nError! We don\'t have that file!')

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
    server = await asyncio.start_server(handle_echo, str(server_address), server_port)

    # keeping server alive over and over again
    async with server:
        await server.serve_forever()


# run program
asyncio.run(main())
