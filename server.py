import socket
from tictactoe import TicTacToe

# creates server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# initiates client/server connection
server.bind(("127.0.0.1", 5000))

# listening for connection
server.listen(0)

# accepts connection
client, addr = server.accept()

gameMode = False
game = ''
message = ''
response = ''
restart = False
indicies = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
invalidMessage = False

while True:
    # receives message and decodes
    message = client.recv(4096)
    message = message.decode()
    print('Client sent -> ' + message)

    # starts game
    if message == 'tic-tac-toe':
        game = TicTacToe('server', 'client')
        print('Client started Tic-Tac-Toe, you go first')
        gameMode = True

    # if client quits
    if message == '/q':
        print("Client has ended chat. Goodbye!")
        break
    # in gameMode
    if gameMode:
        # check clients move and validates
        if message != 'tic-tac-toe':
            if message not in indicies:
                response = 'Invalid input. Please enter number 1-9 that has not been selected'
                client.send(response.encode())
                invalidMessage = True
            else:
                # valid input mark board
                game.setValue(int(message), 'client')
                indicies[int(message) - 1] = ''
                # if client wins
                if game.checkWinner():
                    print("Bummer, client won!")
                    response = 'Congrats you won!' + "\n" + game.printBoard()
                    client.send(response.encode())
                    gameMode = False
                    restart = True
                    indicies = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        # if game not over
        if not restart:
            if not invalidMessage:
                # servers turn
                print(game.printBoard())
                index = input("Enter Game Input -> ")
                # validate server input
                while index not in indicies:
                    print("Invalid input. Please enter number 1-9 that has not been selected")
                    index = input("Enter Game Input -> ")
                # set board and remove index from list
                game.setValue(int(index), "server")
                indicies[int(index) - 1] = ''
                response = game.printBoard()
                client.send(response.encode())

                # server wins
                if game.checkWinner():
                    print("Congrats you won!")
                    gameMode = False
                    restart = True
                    indicies = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            invalidMessage = False
    # in Chat Mode
    if not gameMode:
        # makes sure game isn't just ending
        if not restart:
            response = input("Enter Input ->")
            if len(response) == 0:
                response = ' '
            client.send(response.encode())
        if restart:
            restart = False

    # if server quits
    if response == '/q':
        print('Shutting Down!')
        break

# close socket
server.close()
