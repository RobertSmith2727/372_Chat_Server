class TicTacToe:
    boarder = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, player1, player2):
        self._board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self._player1 = player1
        self._player2 = player2
        self._winner = ''

    def get_player1(self):
        return self._player1

    def get_player2(self):
        return self._player2

    def getBoard(self):
        return self._board

    def checkWinner(self):
        try:
            # 3 down
            for index in range(0, 4, 1):
                if self._board[index] == self._board[index + 3] and self._board[index + 3] == self._board[index + 6]:
                    self.setWinner(self._board[index])
                    return True
            # 3 across
            for index in range(0, 7, 3):
                if self._board[index] == self._board[index + 1] and self._board[index + 1] == self._board[index + 2]:
                    self.setWinner(self._board[index])
                    return True
            if self._board[0] == self._board[4] and self._board[4] == self._board[8]:
                self.setWinner(self._board[0])
                return True
            if self._board[2] == self._board[4] and self._board[4] == self._board[6]:
                self.setWinner(self._board[2])
                return True
        except:
            return False

    def getWinner(self):
        return self._winner

    def setWinner(self, mark):
        if mark == 'X':
            self._winner = self._player1 + " (X's)"
        else:
            self._winner = self._player2 + " (O's)"

    def printBoard(self):
        count = 0
        line = '\n'
        for value in self._board:
            line = line + ' ' + str(value) + ' '
            count += 1
            if count % 3 == 0:
                line = line + '\n'
                if count != 9:
                    line = line + '-----------' + '\n'
            else:
                line = line + '|'
        if self.checkWinner():
            return line + '\n' + self.getWinner() + ' won! To play again enter "tic-tac-toe"'
        return line + '\n' + 'make your move:'

    def setValue(self, index, player):
        if self._board[index - 1] == 'X' or self._board[index - 1] == 'O':
            print('spot already taken')
        if player == self._player1:
            self._board[index - 1] = 'X'
        else:
            self._board[index - 1] = 'O'
# rules
# make board
# get board
#
# r = TicTacToe("server", "client")
# print(r.printBoard())
#
# r.setValue(3, "server")
# print(r.printBoard())
#
# board = r.printBoard()
# for x in board:
#     print(x, 'line')

