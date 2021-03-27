import arcade
import board
import pieces

SCREEN_LENGTH = 800
BOARD_LENGTH = 600

SQUARE_LENGTH = BOARD_LENGTH // 8
OFFSET = (SCREEN_LENGTH - BOARD_LENGTH) // 2


class ChessWindow(arcade.Window):
    def draw_board(self):

        def f(x):
            return x * SQUARE_LENGTH + OFFSET

        for n in range(2):
            for i in range(n, 8, 2):
                for j in range(n, 8, 2):
                    arcade.draw_lrtb_rectangle_filled(
                        f(i), f(i + 1), f(j + 1), f(j), arcade.csscolor.WHITE
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
        arcade.set_background_color(arcade.csscolor.BLACK)

        self.white_list = None
        self.black_list = None
        self._board = None

    def setup(self):
        self.black_list = arcade.SpriteList()
        self.white_list = arcade.SpriteList()

        self._board = [
            [pieces.EMPTY, pieces.Bishop()],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        ]

        self.test_sprite = arcade.Sprite("piece_sprites/2bdab.png", 0.5)
        self.test_sprite.center_x = 200
        self.test_sprite.center_y = 200
        self.white_list.append(self.test_sprite)

    def on_draw(self):
        arcade.start_render()
        self.draw_board()
        self.white_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        print((x - OFFSET) // SQUARE_LENGTH, (y - OFFSET) // SQUARE_LENGTH, button)


if __name__ == "__main__":
    window = ChessWindow()
    window.setup()
    arcade.run()
