import socket
from tictactoe import TicTacToe

# creates client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# initiates client/server connection
client.connect(("127.0.0.1", 5000))

gameMode = False
game = ''
message = ''
response = ''
restart = False
while True:
    # starts game
    if response == 'tic-tac-toe':
        game = TicTacToe('client', 'server')
        print('Server started Tic-Tac-Toe, you go first')
        gameMode = True

    # In Chat Mode
    if not gameMode:
        if not restart:
            # sends message
            message = input("Enter Input -> ")
            if len(message) == 0:
                message = ' '
            client.send(message.encode())
        if restart:
            restart = False

        response = client.recv(4096)
        response = response.decode()
        print('Server sent -> ' + response)

    if gameMode:
        # client's turn
        print(game.printBoard())
        index = input("Enter Game Input -> ")
        game.setValue(int(index), "client")
        message = game.printBoard()
        client.send(message.encode())

        # client wins
        if game.checkWinner():
            print("Congrats you won!")
            gameMode = False
            restart = True

        # Servers turn
        if gameMode:
            response = client.recv(4096)
            response = response.decode()
            game.setValue(int(response), 'server')
            print('Server sent -> ' + response)

            # server wins
            if game.checkWinner():
                print("Bummer, server won!")
                message = 'Congrats you won!' + "\n" + game.printBoard()
                client.send(message.encode())
                gameMode = False
                restart = True

    # if server quits
    if response == '/q':
        print('Server has ended chat. Goodbye!')
        break
    # if client quits
    if message == '/q':
        print('Shutting Down!')
        break


# close socket
client.close()

