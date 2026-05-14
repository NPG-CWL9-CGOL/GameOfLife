import numpy as np
from patterns import get_pattern


class Grid:
    def __init__(self, rows: int = 0, cols: int = 0) -> None:
        """Inicjalizacja siatki o danej wielkości"""
        self._grid: np.ndarray = np.zeros((rows, cols), dtype=np.bool_)

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
