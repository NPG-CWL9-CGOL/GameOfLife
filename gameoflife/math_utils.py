
def point_in_rect(pos, rect) -> bool:
    """Sprawdza, czy punkt (x, y) znajduje się w prostokącie."""
    x, y = pos
    rx, ry, rw, rh = rect
    return rx <= x < rx + rw and ry <= y < ry + rh
