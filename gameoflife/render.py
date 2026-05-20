import pygame

import gameoflife.config as config

from gameoflife.grid import Grid

from gameoflife.ui.components import UIComponent
from gameoflife.ui.views import *

class GameRenderer:
    """Moduł odpowiedzialny za renderowanie obrazu"""
    
    def __init__(self, window_size: tuple[int, int], window_title: str) -> None:
        pygame.display.set_caption(window_title)
        self.screen = pygame.display.set_mode(window_size)

    def render():
        pass


class GridRenderer:
    def __init__(self, screen, grid: Grid, x, y, width, height, cell_size):
        self.screen = screen
        self.grid = grid

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cell_size = cell_size
    

    def render_outline(self):
        """
        Rysuje pustą planszę oraz kontury siatki.
        To realizuje zadanie: renderowanie konturu siatki.
        """
        pygame.draw.rect(
            self.screen,
            config.self.BACKGROUND_COLOR,
            (self.x, self.y, self.width, self.height)
        )

        # Linie pionowe
        for x in range(self.x, self.x + self.width + 1, self.cell_size):
            pygame.draw.line(
                self.screen,
                config.self.LINE_COLOR,
                (x, self.y),
                (x, self.y + self.height)
            )

        # Linie poziome
        for y in range(self.y, self.y + self.height + 1, self.cell_size):
            pygame.draw.line(
                self.screen,
                config.self.LINE_COLOR,
                (self.x, y),
                (self.x + self.width, y)
            )

        pygame.draw.rect(
            self.screen,
            config.self.BORDER_COLOR,
            (self.x, self.y, self.width, self.height),
            2
        )


    def render_cells(self):
        """
        Rysuje żywe komórki na podstawie aktualnego stanu obiektu Grid.
        To realizuje zadanie: wizualizacja stanu komórek na siatce.
        """
        rows, cols = self.grid.shape

        for row in range(rows):
            for col in range(cols):
                if self.grid.data[row, col]:
                    x = self.x + col * self.cell_size
                    y = self.y + row * self.cell_size

                    pygame.draw.rect(
                        self.screen,
                        config.ALIVE_CELL_COLOR,
                        (x + 2, y + 2, self.cell_size - 4, self.cell_size - 4)
                    )
