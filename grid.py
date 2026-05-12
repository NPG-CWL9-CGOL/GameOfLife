import numpy as np

_GRID: np.ndarray = np.zeros((0, 0), dtype=np.bool_)

def init(rows: int, cols: int) -> None:
    global _GRID
    _GRID = np.zeros((rows, cols), dtype=np.bool_)

def assert_init() -> None:
    global _GRID
    if _GRID.size == 0:
        raise RuntimeError("Grid isnt initialized")

def set_cell(x: int, y: int, state: bool) -> None:
    assert_init()
    global _GRID
    
    _GRID[y, x] = state

def toggle_cell(x: int, y: int) -> bool:
    assert_init()
    global _GRID
    
    _GRID[y, x] = not _GRID[y, x]
    return _GRID[y, x]

def get_cell(x: int, y: int) -> bool:
    assert_init()
    global _GRID
    
    return _GRID[y, x]

def set_grid(arr: np.ndarray) -> None:
    global _GRID
    _GRID = arr.astype(np.bool_).copy()

def set_grid_from_active(cells: list[list[int]]) -> None:
    assert_init()
    for x, y in cells:
        set_cell(x, y, True)

def reset_grid() -> None:
    assert_init()
    global _GRID

    _GRID[:] = False
