"""Moduł definiujący struktury danych, geometrię i renderowanie siatki Gry w Życie."""

from __future__ import annotations

import random

import pygame

import numpy as np

from gameoflife import config
from gameoflife.math_utils import point_in_rect
from gameoflife.patterns import get_pattern


class GridData:
    """Klasa przechowująca binarną macierz stanu komórek."""

    def __init__(self, rows: int = 0, cols: int = 0) -> None:
        """Inicjalizacja siatki o danej wielkości"""
        self._grid: np.ndarray = np.zeros((rows, cols), dtype=np.bool_)

    @classmethod
    def from_data(cls, data: np.ndarray) -> GridData:
        """Inicjalizacja obiektu z istniejącej siatki (NIE kopiuje)"""
        grid = cls(*data.shape)
        grid._grid = data

        return grid

    def _assert_init(self) -> None:
        """Sprawdza czy siatka została poprawnie zainicjalizowana."""
        if self._grid.size == 0:
            raise RuntimeError("Grid isn't initialized")

    def init(self, rows: int, cols: int) -> None:
        """Reinicjalizacja siatki o danej wielkości"""
        self._grid = np.zeros((rows, cols), dtype=np.bool_)

    def set_cell(self, x: int, y: int, state: bool) -> None:
        """Ustawienie komórki (x, y) na stan state"""
        self._assert_init()
        self._grid[y, x] = state

    def toggle_cell(self, x: int, y: int) -> bool:
        """Ustawienie komórki (x, y) na stan przeciwny"""
        self._assert_init()
        self._grid[y, x] = not self._grid[y, x]
        return bool(self._grid[y, x])

    def get_cell(self, x: int, y: int) -> bool:
        """Odczytanie stanu komórki (x, y)"""
        self._assert_init()
        return bool(self._grid[y, x])

    def set_grid(self, arr: np.ndarray) -> None:
        """Ustawienie siatki z innej siatki (kopiuje)"""
        self._grid = arr.astype(np.bool_).copy()

    def set_grid_from_active(self, cells: list[tuple[int, int]]) -> None:
        """Ustawienie siatki z listy aktywnych komórek"""
        self._assert_init()
        for x, y in cells:
            self.set_cell(x, y, True)

    def reset_grid(self) -> None:
        """Wyczyszczenie siatki do stanu początkowego (same '0')"""
        self._assert_init()
        self._grid[:] = False

    def place_pattern(self, pattern_name: str, start_x: int, start_y: int) -> bool:
        """Umieszczenie wzoru na siatce począwszy od pozycji (start_x, start_y).
        Zwraca True jeśli się udało, False jeśli wzór wychodzi poza granice."""
        self._assert_init()
        pattern = get_pattern(pattern_name)
        if not pattern:
            return False
        
        rows, cols = self._grid.shape
        for dx, dy in pattern:
            x, y = start_x + dx, start_y + dy
            if 0 <= x < cols and 0 <= y < rows:
                self.set_cell(x, y, True)
            else:
                return False  
        return True

    @property
    def shape(self) -> tuple[int, ...]:
        """Zwraca wymiary siatki (wiersze, kolumny)."""
        return self._grid.shape

    @property
    def data(self) -> np.ndarray:
        """Zwraca surowe dane siatki jako macierz NumPy."""
        return self._grid



class GridGeometry:
    """Klasa definiująca położenie i rozmiar siatki w przestrzeni okna."""

    def __init__(self, grid_data: GridData, x: int, y: int, width: int, height: int, cell_size: int):
        self.grid_data = grid_data

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cell_size = cell_size

    def get_cell(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        """Przelicza współrzędne pikselowe na indeksy komórki (kolumna, wiersz)."""
        mx, my = pos
        if not (self.x <= mx < self.x + self.width and self.y <= my < self.y + self.height):
            return None

        col = (mx - self.x) // self.cell_size
        row = (my - self.y) // self.cell_size
        return col, row


    def draw_line(self, start_cell: tuple[int, int], end_cell: tuple[int, int], state: bool) -> None:
        """Rysuje linię komórek między dwoma punktami na siatce."""
        
        x0, y0 = start_cell
        x1, y1 = end_cell
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.grid_data.set_cell(x0, y0, state)
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy



class GridRenderer:
    """Klasa odpowiedzialna za graficzne przedstawienie siatki na ekranie."""

    def __init__(self, screen: pygame.Surface):
        """Inicjalizuje renderer z dostępem do powierzchni ekranu."""
        self.screen = screen
        

    def render_outline(self, grid_geometry: GridGeometry) -> None:
        """
        Rysuje pustą planszę oraz kontury siatki.
        To realizuje zadanie: renderowanie konturu siatki.
        """
        pygame.draw.rect(
            self.screen,
            config.BACKGROUND_COLOR,
            (grid_geometry.x, grid_geometry.y, grid_geometry.width, grid_geometry.height)
        )

        # Linie pionowe
        for x in range(grid_geometry.x, grid_geometry.x + grid_geometry.width + 1, grid_geometry.cell_size):
            pygame.draw.line(
                self.screen,
                config.GRID_LINE_COLOR,
                (x, grid_geometry.y),
                (x, grid_geometry.y + grid_geometry.height)
            )

        # Linie poziome
        for y in range(grid_geometry.y, grid_geometry.y + grid_geometry.height + 1, grid_geometry.cell_size):
            pygame.draw.line(
                self.screen,
                config.GRID_LINE_COLOR,
                (grid_geometry.x, y),
                (grid_geometry.x + grid_geometry.width, y)
            )

        pygame.draw.rect(
            self.screen,
            config.GRID_BORDER_COLOR,
            (grid_geometry.x, grid_geometry.y, grid_geometry.width, grid_geometry.height),
            2
        )


    def render_cells(self, grid_data: GridData, grid_geometry: GridGeometry) -> None:
        """
        Rysuje żywe komórki na podstawie aktualnego stanu obiektu Grid.
        To realizuje zadanie: wizualizacja stanu komórek na siatce.
        """
        rows, cols = grid_data.shape

        for row in range(rows):
            for col in range(cols):
                if grid_data.get_cell(x=col, y=row):
                    x = grid_geometry.x + col * grid_geometry.cell_size
                    y = grid_geometry.y + row * grid_geometry.cell_size

                    pygame.draw.rect(
                        self.screen,
                        config.ALIVE_CELL_COLOR,
                        (x + 2, y + 2, grid_geometry.cell_size - 4, grid_geometry.cell_size - 4)
                    )



def fill_grid_randomly(grid: GridData, chance: float = 0.2) -> None:
    """Losowo ustawia część komórek jako żywe, żeby było co wizualizować."""
    rows, cols = grid.shape

    for row in range(rows):
        for col in range(cols):
            if random.random() < chance:
                grid.set_cell(col, row, True)
