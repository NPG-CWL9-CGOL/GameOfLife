import pygame

import numpy as np

import gameoflife.config as config
from gameoflife.patterns import get_pattern



class GridData:
    def __init__(self, rows: int = 0, cols: int = 0) -> None:
        """Inicjalizacja siatki o danej wielkości"""
        self._grid: np.ndarray = np.zeros((rows, cols), dtype=np.bool_)

    @classmethod
    def from_data(cls, data: np.ndarray):
        """Inicjalizacja obiektu z istniejącej siatki (NIE kopiuje)"""
        grid = cls(*data.shape)
        grid._grid = data

        return grid

    def _assert_init(self) -> None:
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
        return self._grid.shape

    @property
    def data(self) -> np.ndarray:
        return self._grid



class GridGeometry:
    def __init__(self, grid_data: GridData, x, y, width, height, cell_size):
        self.grid_data = grid_data

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cell_size = cell_size


    def get_cell(self, pos):
        mx, my = pos
        if not (self.x <= mx < self.x + self.width and self.y <= my < self.y + self.height):
            return None

        col = (mx - self.x) // self.cell_size
        row = (my - self.y) // self.cell_size
        return col, row


    #teraz zwracamy stan pędzla zamiast togglowania pojedynczej komorki
    def handle_grid_click(self, event, exclude_ui_rects, editing):
        """Obsługa kliknięcia w siatkę, z pominięciem obszarów UI.
        Zwraca stan pędzla dla przeciągania komórek."""

        if editing is False:
            return None, None

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None, None

        if any(GridGeometry.point_in_rect(event.pos, rect) for rect in exclude_ui_rects):
            return None, None

        cell = self.get_cell(event.pos, self.x, self.y, self.width, self.height, self.cell_size)
        
        if cell is None:
            return None, None

        col, row = cell
        current_state = self.grid_data.get_cell(col, row)
        target_state = not current_state
        #draw_line_on_grid(grid, cell, cell, target_state)
        
        return target_state, cell


    @staticmethod
    def point_in_rect(pos, rect) -> bool:
        """Sprawdza, czy punkt (x, y) znajduje się w prostokącie."""
        x, y = pos
        rx, ry, rw, rh = rect
        return rx <= x < rx + rw and ry <= y < ry + rh



class GridRenderer:
    def __init__(self, screen, grid_data: GridData, grid_geometry: GridGeometry):
        self.screen = screen
        
        self.grid_data = grid_data
        self.grid_geometry = grid_geometry


    def render_outline(self):
        """
        Rysuje pustą planszę oraz kontury siatki.
        To realizuje zadanie: renderowanie konturu siatki.
        """
        pygame.draw.rect(
            self.screen,
            config.BACKGROUND_COLOR,
            (self.x, self.y, self.width, self.height)
        )

        # Linie pionowe
        for x in range(self.x, self.x + self.width + 1, self.cell_size):
            pygame.draw.line(
                self.screen,
                config.LINE_COLOR,
                (x, self.y),
                (x, self.y + self.height)
            )

        # Linie poziome
        for y in range(self.y, self.y + self.height + 1, self.cell_size):
            pygame.draw.line(
                self.screen,
                config.LINE_COLOR,
                (self.x, y),
                (self.x + self.width, y)
            )

        pygame.draw.rect(
            self.screen,
            config.BORDER_COLOR,
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
                if self.grid_data.get_cell(row, col):
                    x = self.x + col * self.cell_size
                    y = self.y + row * self.cell_size

                    pygame.draw.rect(
                        self.screen,
                        config.ALIVE_CELL_COLOR,
                        (x + 2, y + 2, self.cell_size - 4, self.cell_size - 4)
                    )
