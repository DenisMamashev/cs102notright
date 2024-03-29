import pygame
import random
import copy
from copy import deepcopy


from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize == True:
            self.grid = [[random.randint(0, 1) for i in range(self.cell_width)] for j in range(self.cell_height)]
        else:
            self.grid = [[0 for i in range(self.cell_width)] for j in range(self.cell_height)]
        return self.grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_width):
            for col in range(self.cell_height):
                if self.grid[col][row]:
                    pygame.draw.rect(self.screen,pygame.Color("green"),
                        (
                            self.cell_size * row + 1,
                            self.cell_size * col + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )
                else:
                    pygame.draw.rect(self.screen,pygame.Color("white"),
                        (
                            self.cell_size * row + 1,
                            self.cell_size * col + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        col, row = cell
        for pos_y in range(col - 1, col + 2):
            for pos_x in range(row - 1, row + 2):
                if not (0 <= pos_y <= self.cell_height - 1 and 0 <= pos_x <= self.cell_width - 1) or (pos_y == col and pos_x == row):
                    continue
                neighbours.append(self.grid[pos_y][pos_x])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_array = copy.deepcopy(self.grid)
        for col in range(self.cell_height):
            for row in range(self.cell_width):
                cell = col, row
                if sum(self.get_neighbours(cell)) == 3:
                    new_array[col][row] = 1
                elif sum(self.get_neighbours(cell)) == 2:
                    continue
                else:
                    if self.grid[col][row] == 1:
                        new_array[col][row] = 0
        self.grid = new_array
        return self.grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
