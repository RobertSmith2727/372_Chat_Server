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
indicies = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
invalidMessage = False
while True:
    # starts game logic
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

    # In gameMode
    if gameMode:
        # if server input invalid
        if invalidMessage:
            res = 'Invalid input. Please enter number 1-9 that has not been selected'
            client.send(res.encode())
        else:
            # client's turn
            print(game.printBoard())
            index = input("Enter Game Input -> ")
            # validate client input
            while index not in indicies:
                print("Invalid input. Please enter number 1-9 that has not been selected")
                index = input("Enter Game Input -> ")
            # set board
            game.setValue(int(index), "client")
            # remove index from list
            indicies[int(index) - 1] = ''
            message = game.printBoard()
            client.send(message.encode())

        invalidMessage = False

        # client wins
        if game.checkWinner():
            print("Congrats you won!")
            gameMode = False
            restart = True
            indicies = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        # Servers turn
        if gameMode:
            response = client.recv(4096)
            response = response.decode()
            # activate invalid message logic
            if response not in indicies:
                invalidMessage = True
            if not invalidMessage:
                # set board and remove index from list
                game.setValue(int(response), 'server')
                indicies[int(response) - 1] = ''
                print('Server sent -> ' + response)

                # server wins
                if game.checkWinner():
                    print("Bummer, server won!")
                    message = 'Congrats you won!' + "\n" + game.printBoard()
                    client.send(message.encode())
                    gameMode = False
                    restart = True
                    indicies = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

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

