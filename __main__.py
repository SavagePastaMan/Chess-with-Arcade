import arcade
import pieces

SCREEN_LENGTH = 800
BOARD_LENGTH = 600

SQUARE_LENGTH = BOARD_LENGTH // 8
OFFSET = (SCREEN_LENGTH - BOARD_LENGTH) // 2
INITIAL_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNRR"


def coor2pos(coor: float) -> float:
    return coor * SQUARE_LENGTH + OFFSET


def pos2coor(pos: float) -> float:
    return (pos - OFFSET) // SQUARE_LENGTH


def center_on_square(point: tuple[float, float]) -> tuple[float, float]:
    x, y = point
    sx = coor2pos(pos2coor(x))
    sy = coor2pos(pos2coor(y))
    return sx + SQUARE_LENGTH // 2, sy + SQUARE_LENGTH // 2


class ChessWindow(arcade.Window):
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = arcade.csscolor.WHITE
                else:
                    color = arcade.csscolor.GRAY

                arcade.draw_lrtb_rectangle_filled(
                    coor2pos(i), coor2pos(i + 1), coor2pos(j + 1), coor2pos(j), color
                )

        # outline board so black squares on border don't look shit
        arcade.draw_lrtb_rectangle_outline(
            OFFSET,
            SCREEN_LENGTH - OFFSET,
            SCREEN_LENGTH - OFFSET,
            OFFSET,
            arcade.csscolor.WHITE,
        )

    def __init__(self):
        super().__init__(SCREEN_LENGTH, SCREEN_LENGTH, "Chess")
        arcade.set_background_color(arcade.csscolor.LIGHT_BLUE)

        self.white = None
        self.black = None

        # the piece referenced by `self.grabbed` is slaved to the mouse position
        self.grabbed = None
        self.taken_from_x = None
        self.taken_from_y = None

    def setup(self):
        self.white = arcade.SpriteList()
        self.black = arcade.SpriteList()

        fen = INITIAL_POSITION.split("/")
        piece_map = dict(
            p=pieces.Pawn,
            r=pieces.Rook,
            n=pieces.Knight,
            b=pieces.Bishop,
            q=pieces.Queen,
            k=pieces.King,
        )
        for j, row in enumerate(fen):
            for i, char in enumerate(row):
                if char == '8':
                    continue
                piece = piece_map[char.lower()]
                color = pieces.Color.BLACK if char.islower() else pieces.Color.WHITE
                getattr(self, color.name.lower()).append(
                    piece(
                        color,
                        OFFSET + SQUARE_LENGTH * i + SQUARE_LENGTH // 2,
                        OFFSET + SQUARE_LENGTH * j + SQUARE_LENGTH // 2,
                    )
                )

    def on_draw(self):
        arcade.start_render()
        self.draw_board()
        self.white.draw()
        self.black.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        # if we aren't holding a piece, pick up the piece at the square
        # that we clicked, or None if it doesn't exist
        if self.grabbed is None:
            intersection = arcade.get_sprites_at_point(
                (x, y), self.white
            ) or arcade.get_sprites_at_point((x, y), self.black)

            if intersection:
                # there should never be two pieces in the same square
                (self.grabbed,) = intersection

                # if the square we try to drop it at is invalid,
                # return it to this location
                cx, cy = center_on_square((x, y))
                self.taken_from_x = cx
                self.taken_from_y = cy

                self.grabbed.center_x = x
                self.grabbed.center_y = y
        else:
            cx, cy = center_on_square((x, y))
            coord_x = pos2coor(cx)
            coord_y = pos2coor(cy)
            # capture a piece by removing it from the sprite list
            if (coord_x, coord_y) in self.grabbed.possible_moves():
                if self.grabbed.piece_color is pieces.Color.WHITE:
                    if piece := arcade.get_sprites_at_point((x, y), self.black):
                        self.black.remove(*piece)
                elif self.grabbed.piece_color is pieces.Color.BLACK:
                    if piece := arcade.get_sprites_at_point((x, y), self.white):
                        self.white.remove(*piece)
                self.grabbed.center_x = cx
                self.grabbed.center_y = cy
            else:
                self.grabbed.center_x = self.taken_from_x
                self.grabbed.center_y = self.taken_from_y
                self.taken_from_x = None
                self.taken_from_y = None

            # drop the reference to the held piece,
            # so it is no longer pulled along with the mouse
            self.grabbed = None

    def on_mouse_motion(self, x, y, dx, dy):
        if self.grabbed:
            self.grabbed.center_x = x
            self.grabbed.center_y = y


if __name__ == "__main__":
    window = ChessWindow()
    window.setup()
    arcade.run()
