import numpy as np
from scipy.signal import convolve2d
from grid import Grid

_KERNEL = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
], dtype=np.uint8)


class Engine:
    """Moduł odpowiedzialny za przeprowadzenie symulacji"""

    def __init__(self, grid: Grid):
        self.grid = grid

    def update(self) -> None:
        """Aktualizacja stanu siatki - kolejny krok w symulacji"""

        neighbors = convolve2d(
            self.grid.data.view(np.uint8),
            _KERNEL,
            mode='same',
            boundary='wrap'
        )

        # Zasady:
        #   kazda komorka z 3 sasiadami -> zyje (rodzi sie badz pozostaje zywa)
        #   zyjaca komorka z 2 sasiadami -> pozostaje zywa
        #   pozostale -> martwe
        
        np.logical_or(
            neighbors == 3,
            np.logical_and(self.grid.data, neighbors == 2),
            out=self.grid.data
        )