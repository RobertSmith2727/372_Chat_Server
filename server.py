import socket


# creates server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# initiates client/server connection
server.bind(("127.0.0.1", 5000))

# listening for connection
server.listen(0)

# accepts connection
client, addr = server.accept()

while True:
    # receives message
    message = client.recv(4096)
    # decodes
    message = message.decode()
    print('Client sent -> ' + message)
    # if client quits
    if message == '/q':
        print("Client has ended chat. Goodbye!")
        # tells client server ended chat
        break

    response = input("Enter Input ->")
    if len(response) == 0:
        response = ' '
    client.send(response.encode())

    # if server quits
    if response == '/q':
        print('Shutting Down!')
        break

# close sockets
# client.close()
server.close()
