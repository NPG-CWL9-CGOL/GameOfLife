import numpy as np

_GRID: np.ndarray = np.zeros((0, 0), dtype=np.bool_)

def init(rows: int, cols: int) -> None:
    """Initalizacja siatki o danej wielkosci"""
    global _GRID
    _GRID = np.zeros((rows, cols), dtype=np.bool_)

def assert_init() -> None:
    global _GRID
    if _GRID.size == 0:
        raise RuntimeError("Grid isnt initialized")

def set_cell(x: int, y: int, state: bool) -> None:
    """Ustawienie komorki (x, y) na stan state"""
    assert_init()
    global _GRID
    
    _GRID[y, x] = state

def toggle_cell(x: int, y: int) -> bool:
    """Ustawienie komorki (x, y) na stan przeciwny"""
    assert_init()
    global _GRID
    
    _GRID[y, x] = not _GRID[y, x]
    return _GRID[y, x]

def get_cell(x: int, y: int) -> bool:
    """Odczytanie stanu komorki (x, y)"""
    assert_init()
    global _GRID
    
    return _GRID[y, x]

def set_grid(arr: np.ndarray) -> None:
    """Ustawienie siatki z innej siatki (kopiuje)"""
    global _GRID
    _GRID = arr.astype(np.bool_).copy()

def set_grid_from_active(cells: list[tuple[int, int]]) -> None:
    """Ustawienie siatki z listy aktywnych komorek"""
    assert_init()
    for x, y in cells:
        set_cell(x, y, True)

def reset_grid() -> None:
    """Wyczyszczenie siatki do stanu poczatkowego (same '0')"""
    assert_init()
    global _GRID

    _GRID[:] = False
