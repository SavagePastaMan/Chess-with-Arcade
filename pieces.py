from enum import Enum, auto
from abc import ABC, abstractmethod


class Color(Enum):
    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()


class Piece(ABC):
    @abstractmethod
    def possible_moves(self):
        pass

    @abstractmethod
    def __repr__(self):
        return f"<Piece {self.color.name} "

    @abstractmethod
    def __init__(self, color: Color, x: int, y: int):
        # 0 is white, 1 is black
        self.color = color
        self.x = x
        self.y = y


class __Empty(Piece):
    def possible_moves(self):
        ...

    def __repr__(self):
        return super().__repr__() + "'E'>"

    def __init__(self, color, x, y):
        super().__init__(color, x, y)


EMPTY = __Empty(Color.WHITE, 0, 0)


class Pawn(Piece):
    def possible_moves(self):
        ...

    def __init__(self, color: Color, x, y):
        super().__init__(color, x, y)

    def __repr__(self):
        return super().__repr__() + "'P'>"


class Bishop(Piece):
    def possible_moves(self):
        ...

    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def __repr__(self):
        return super().__repr__() + "'B'>"


class Knight(Piece):
    def possible_moves(self):
        ...

    def __init__(self, color: Color, x, y):
        super().__init__(color, x, y)

    def __repr__(self):
        return super().__repr__() + "'N'>"


class Queen(Piece):
    def __init__(self, color: Color, x, y):
        super().__init__(color, x, y)

    def __repr__(self):
        return super().__repr__() + "'Q'>"

    def possible_moves(self):
        pass
