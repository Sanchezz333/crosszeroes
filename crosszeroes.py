from enum import Enum
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
        

class GameField:
    def __init__(self) -> None:
        self.height = 3
        self.width = 3
        self.cells = [[Cell.VOID]*self.width for i in range(self.height)]


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
    
    def draw(self):
        for i in range(self._field.height):
            for j in range(self._field.width):
                cur_pos_x = self._x + j*CELL_SIZE
                cur_pos_y = self._y + i*CELL_SIZE
                pygame.draw.rect(self._screen, (255,255,255), (cur_pos_x, cur_pos_y, CELL_SIZE, CELL_SIZE),1)
                if self._field.cells[i][j] == Cell.ZERO:
                    pygame.draw.circle(self._screen, (255,255,255), (cur_pos_x+CELL_SIZE/2, cur_pos_y+CELL_SIZE/2), (CELL_SIZE-20)/2, 1)
                if self._field.cells[i][j] == Cell.CROSS:
                    pygame.draw.rect(self._screen, (255,255,255), (cur_pos_x+10 , cur_pos_y+10, CELL_SIZE-20, CELL_SIZE-20),1)
    def check_coords_correct(self, x, y):        
        return x - self._x < self._width and y - self._y < self._height and x > self._x and y > self._y

    def get_coords(self, x, y):
        return ((y - self._y) // CELL_SIZE, (x - self._x) // CELL_SIZE)

class GameRoundManager:
    """
    Менеджер игры, запускающий все процессы.
    """
    def __init__(self, player1: Player, player2: Player):
        self._players = [player1, player2]
        self._current_player = 0
        self.field = GameField()
        

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
        cur_state = True
        for i in range(self.field.height):
            for j in range(self.field.width):
                cur_state =  cur_state and self.field.cells[i][j] != Cell.VOID
        return cur_state


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
        
        # Window
        self._width = 800
        self._height = 600
        self._title = "Crosses and Zeroes"
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(self._title)
        self.player1 = Player("Петя", Cell.CROSS)
        self.player2 = Player("Вася", Cell.ZERO)
        self._game_manager = GameRoundManager(self.player1, self.player2)
        self._field_widget = GameFieldView(self._game_manager.field, self._screen, 100, 100)
    
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
                text = self.font.render(f'{self.player1.name} is win', True, (255, 255, 255))
                self._screen.blit(text, (100, 30))
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
                

            self._field_widget.draw()
            pygame.display.flip()
            clock.tick(FPS)

    def new_game(self):
        print("New game!")
        self._game_manager = GameRoundManager(self.player1, self.player2)
        self._field_widget = GameFieldView(self._game_manager.field, self._screen, 100, 100)

def main():
    window = GameWindow()
    window.main_loop()
    print("Game over!")

if __name__ == "__main__":
    main()