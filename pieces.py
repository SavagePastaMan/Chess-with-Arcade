import arcade
from enum import Enum, auto
from abc import ABC, abstractmethod


class Color(Enum):
    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()


class Piece(ABC, arcade.Sprite):
    @abstractmethod
    def possible_moves(self):
        pass

    @abstractmethod
    def __repr__(self):
        return f"<Piece {self.piece_color.name} "

    @abstractmethod
    def __init__(self, filename: str, color: Color, x: int, y: int):
        super().__init__(filename=filename, center_x=x, center_y=y, scale=0.5)
        self.piece_color = color
        self.center_x = x
        self.center_y = y


class __Empty(Piece):
    def possible_moves(self):
        ...

    def __repr__(self):
        return super().__repr__() + "'E'>"

    def __init__(self, color, x, y):
        super().__init__("piece_sprites/2bdab.png", color, x, y)


EMPTY = __Empty(Color.WHITE, 0, 0)


class Pawn(Piece):
    def possible_moves(self):
        ...

    def __init__(self, color: Color, x, y):
        super().__init__("piece_sprites/2bdab.png", color, x, y)

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
