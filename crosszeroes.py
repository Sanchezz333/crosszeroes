from enum import Enum
from this import s
import pygame

CELL_SIZE = 50
FPS = 60


class Cell(Enum):
    VOID = 0
    CROSS = 1
    ZERO = 2


class Player:
    """
    Класс игрока, содержит тип значков и имя.
    """

    def __init__(self, name, cell_type) -> None:
        self.name = name
        self.cell_type = cell_type
        self.wins = 0

    def win(self):
        self.wins += 1


class GameField:
    def __init__(self, size) -> None:
        self.height = size
        self.width = size
        self.cells = [[Cell.VOID] * self.width for i in range(self.height)]

    def have_line(self, val, sign):
        if val > self.height or val > self.width:
            return False
        line = False
        for i in range(self.height - val + 1):
            for j in range(self.width - val + 1):
                line = line or self.check_linse(i, j, val, sign)

        return line

    def check_linse(self, i_s, j_s, val, sign):
        r_diag = True
        l_diag = True
        str_ch = False
        col_ch = False
        for i in range(val):
            r_diag = r_diag and self.cells[i_s + i][j_s + i] == sign
            l_diag = l_diag and self.cells[i_s + i][j_s + val - i - 1] == sign
            s_buf = True
            c_buf = True
            for j in range(val):
                s_buf = s_buf and self.cells[i_s + i][j_s + j] == sign
                c_buf = c_buf and self.cells[i_s + j][j_s + i] == sign
            str_ch = str_ch or s_buf
            col_ch = col_ch or c_buf
        return r_diag or l_diag or str_ch or col_ch


class GameFieldView:
    """
    Виджет игрового поля, который отображает его на экране, а также выясняет место клика
    """

    def __init__(self, field, screen, x, y) -> None:
        # загрузить картинки начков клеток...
        # отобразить первичное состояние поля
        self._field = field
        self._height = field.height * CELL_SIZE
        self._width = field.width * CELL_SIZE
        self._screen = screen
        self._x = x
        self._y = y

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def draw(self):
        for i in range(self._field.height):
            for j in range(self._field.width):
                cur_pos_x = self._x + j * CELL_SIZE
                cur_pos_y = self._y + i * CELL_SIZE
                pygame.draw.rect(
                    self._screen,
                    (255, 255, 255),
                    (cur_pos_x, cur_pos_y, CELL_SIZE, CELL_SIZE),
                    1,
                )
                if self._field.cells[i][j] == Cell.ZERO:
                    pygame.draw.circle(
                        self._screen,
                        (255, 255, 255),
                        (cur_pos_x + CELL_SIZE / 2, cur_pos_y + CELL_SIZE / 2),
                        (CELL_SIZE - 20) / 2,
                        1,
                    )
                if self._field.cells[i][j] == Cell.CROSS:
                    pygame.draw.rect(
                        self._screen,
                        (255, 255, 255),
                        (
                            cur_pos_x + 10,
                            cur_pos_y + 10,
                            CELL_SIZE - 20,
                            CELL_SIZE - 20,
                        ),
                        1,
                    )

    def check_coords_correct(self, x, y):
        return (
            x - self._x < self._width
            and y - self._y < self._height
            and x > self._x
            and y > self._y
        )

    def get_coords(self, x, y):
        return ((y - self._y) // CELL_SIZE, (x - self._x) // CELL_SIZE)


class GameRoundManager:
    """
    Менеджер игры, запускающий все процессы.
    """

    def __init__(self, player1: Player, player2: Player, field_size=3):
        self._players = [player1, player2]
        self._current_player = 0
        self.field = GameField(field_size)
        self._winner = "No one"

    def get_current_name(self):
        return self._players[self._current_player].name

    def get_winner_name(self):
        return self._winner

    def handle_click(self, i, j):
        player = self._players[self._current_player]
        # игрок делает клик на поле
        print("click_handled", i, j)
        if self.field.cells[i][j] == Cell.VOID:
            self.field.cells[i][j] = player.cell_type
            if self._current_player == 0:
                self._current_player = 1
            else:
                self._current_player = 0

    def is_game_over(self):
        field_is_full = True
        for i in range(self.field.height):
            for j in range(self.field.width):
                field_is_full = field_is_full and self.field.cells[i][j] != Cell.VOID
        # TODO: Сделать проверку победителя
        somebody_win = False
        for p in self._players:
            if self.field.have_line(3, p.cell_type):
                somebody_win = True
                self._winner = p.name
                p.win()
        return field_is_full or somebody_win


class GameWindow:
    """
    Содержит в себе виджет поля,
    а также менеджер игрового раунда.
    """

    def __init__(self) -> None:
        # инициализация pygame
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self._width = 800
        self._height = 600
        self._title = "Crosses and Zeroes"
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(self._title)
        self.player1 = Player("Петя", Cell.CROSS)
        self.player2 = Player("Вася", Cell.ZERO)
        self._game_manager = GameRoundManager(self.player1, self.player2, 3)
        self._field_widget = GameFieldView(
            self._game_manager.field, self._screen, 100, 100
        )

    def new_game(self):
        print("New game!")
        field_size = 3  # int(input("Введите размер поля"))
        self._game_manager = GameRoundManager(self.player1, self.player2, field_size)
        self._field_widget = GameFieldView(
            self._game_manager.field, self._screen, 100, 100
        )

    def table_drow(self, x, y):
        pygame.draw.circle(
            self._screen,
            (255, 255, 255),
            (x + CELL_SIZE / 2, y + CELL_SIZE / 2),
            (CELL_SIZE - 20) / 2,
            1,
        )
        pygame.draw.rect(
            self._screen,
            (255, 255, 255),
            (x + 10, y + 60, CELL_SIZE - 20, CELL_SIZE - 20),
            1,
        )
        player1 = self.font.render(
            f"{self.player1.name} {self.player1.wins}", True, (255, 255, 255)
        )
        player2 = self.font.render(
            f"{self.player2.name} {self.player2.wins}", True, (255, 255, 255)
        )
        self._screen.blit(
            player1 if self.player1.cell_type == Cell.ZERO else player2,
            (x + 60, y + 10),
        )
        self._screen.blit(
            player1 if self.player2.cell_type == Cell.ZERO else player2,
            (x + 60, y + 60),
        )

    def turn_table_drow(self, x, y):
        player = self._game_manager.get_current_name()
        text = self.font.render(f"{player}'s turn", True, (255, 255, 255))
        self._screen.blit(text, (x + 10, y + 30))

    def winner_drow(self, x, y):
        player = self._game_manager.get_winner_name()
        text = self.font.render(f"{player}' is win", True, (0, 255, 0))
        self._screen.blit(text, (x + 10, y + 30))

    def main_loop(self):
        finished = False
        clock = pygame.time.Clock()
        while not finished:
            self._screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = mouse_pos
                    if self._field_widget.check_coords_correct(x, y):
                        i, j = self._field_widget.get_coords(x, y)
                        self._game_manager.handle_click(i, j)

            if self._game_manager.is_game_over():
                print("Game over!")
                self.winner_drow(
                    150 + self._field_widget.get_width(),
                    50 + self._field_widget.get_height() / 2,
                )
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            finished = True
                            pause = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pause = False
                    self._field_widget.draw()
                    pygame.display.flip()
                    clock.tick(FPS)

                self.new_game()

            self.table_drow(100, 0)
            self.turn_table_drow(100, 100 + self._field_widget.get_height())
            self._field_widget.draw()
            pygame.display.flip()
            clock.tick(FPS)


def main():
    window = GameWindow()
    window.main_loop()
    print("Game over!")


if __name__ == "__main__":
    main()
