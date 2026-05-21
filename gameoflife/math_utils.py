"""Pomocnicze funkcje matematyczne i geometryczne."""

def point_in_rect(pos: tuple[int, int], rect: tuple[int, int, int, int]) -> bool:
    """Sprawdza, czy punkt (x, y) znajduje się w prostokącie."""
    x, y = pos
    rx, ry, rw, rh = rect
    return rx <= x < rx + rw and ry <= y < ry + rh
