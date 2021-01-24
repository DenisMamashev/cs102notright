import pathlib
import random
import copy
from copy import deepcopy

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool = True,
        max_generations: Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize == True:
            matrix = [[random.randint(0, 1) for i in range(self.cols)]for j in range(self.rows)]
        else:
            matrix = [[0 for i in range(self.cols)] for j in range(self.rows)]
        return matrix

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        row, col = cell
        for pos_y in range(row - 1, row + 2):
            for pos_x in range(col - 1, col + 2):
                if not (0 <= pos_y <= self.rows - 1 and 0 <= pos_x <= self.cols - 1) or (pos_y == row and pos_x == col):
                    continue
                neighbours.append(self.curr_generation[pos_y][pos_x])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_array = copy.deepcopy(self.curr_generation)
        for col in range(self.rows):
            for row in range(self.cols):
                cell = col, row
                if sum(self.get_neighbours(cell)) == 3:
                    new_array[col][row] = 1
                elif sum(self.get_neighbours(cell)) == 2:
                    continue
                else:
                    if self.curr_generation[col][row] == 1:
                        new_array[col][row] = 0
        self.grid = new_array
        return self.grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            if self.generations >= self.max_generations:
                return True
            else:
                return False
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation != self.prev_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        new_array = []
        for row in open(filename):
            for part in row:
                if part == "0" or part == "1":
                    new_array.append([int(part)])
        ggame = GameOfLife((len(new_array), len(new_array[0])))
        ggame.curr_generation = new_array
        return ggame

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        for row in self.curr_generation:
            for col in row:
                file.write(str(col))
            file.write("\n")
        file.close()
