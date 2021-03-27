import pieces


class Board:
    def __init__(self):
        self._board = [[pieces.EMPTY for j in range(8)] for i in range(8)]

    def pprint(self):
        print(*self._board, sep="\n")
