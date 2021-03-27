import arcade
import board
import pieces

SCREEN_LENGTH = 800
BOARD_LENGTH = 600

SQUARE_LENGTH = BOARD_LENGTH // 8
OFFSET = (SCREEN_LENGTH - BOARD_LENGTH) // 2


def coor2pos(coor):
    return coor * SQUARE_LENGTH + OFFSET


def pos2coor(pos):
    return (pos - OFFSET) // SQUARE_LENGTH


class ChessWindow(arcade.Window):
    def draw_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = arcade.csscolor.WHITE
                else:
                    color = arcade.csscolor.GRAY

                arcade.draw_lrtb_rectangle_filled(
                    coor2pos(i),
                    coor2pos(i + 1),
                    coor2pos(j + 1),
                    coor2pos(j),
                    color
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

    def setup(self):
        self.white = arcade.SpriteList()
        self.white.append(
            pieces.Pawn(
                pieces.Color.WHITE,
                OFFSET + SQUARE_LENGTH // 2,
                OFFSET + SQUARE_LENGTH // 2,
            )
        )
        self.white.append(
            pieces.Pawn(
                pieces.Color.WHITE,
                OFFSET + SQUARE_LENGTH + SQUARE_LENGTH // 2,
                OFFSET + SQUARE_LENGTH // 2,
                )
        )
        self.black = arcade.SpriteList()

    def on_draw(self):
        arcade.start_render()
        self.draw_board()
        self.white.draw()

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

                self.grabbed.center_x = x
                self.grabbed.center_y = y
        else:
            # snap the position to the center of the closest square
            sx = coor2pos(pos2coor(x))
            sy = coor2pos(pos2coor(y))
            self.grabbed.center_x = sx + SQUARE_LENGTH // 2
            self.grabbed.center_y = sy + SQUARE_LENGTH // 2
            # drop the reference to the held piece,
            # so it is no longer pulled along with the mouse
            self.grabbed = None

            print(pos2coor(x), pos2coor(y))

    def on_mouse_motion(self, x, y, dx, dy):
        if self.grabbed:
            self.grabbed.center_x = x
            self.grabbed.center_y = y


if __name__ == "__main__":
    window = ChessWindow()
    window.setup()
    arcade.run()
