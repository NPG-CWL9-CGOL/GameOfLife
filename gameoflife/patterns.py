from __future__ import annotations

#wzory podawane jako listy krotek wzgledem wspolrzednych startowych 
PATTERNS = {
    "oscillators": {
        "blinker": [(0, 0), (1, 0), (2, 0)], 
        "beacon": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3), (3, 2), (3, 3)], 
        "toad": [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)],  
        "pulsar": [ 
            (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
            (0, 2), (5, 2), (7, 2), (12, 2),
            (0, 3), (5, 3), (7, 3), (12, 3),
            (0, 4), (5, 4), (7, 4), (12, 4),
            (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
            (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
            (0, 8), (5, 8), (7, 8), (12, 8),
            (0, 9), (5, 9), (7, 9), (12, 9),
            (0, 10), (5, 10), (7, 10), (12, 10),
            (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12)
        ]
    },
    "spaceships": {
        "glider": [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]  
    },
    "still_lifes": {
        "block": [(0, 0), (0, 1), (1, 0), (1, 1)],  
        "beehive": [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2)],
        "loaf": [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (3, 2), (2, 3)], 
        "boat": [(0, 0), (1, 0), (0, 1), (2, 1), (1, 2)],  
        "tub": [(1, 0), (0, 1), (2, 1), (1, 2)]  
    }
}

def get_pattern(name: str) -> list[tuple[int, int]]:
    """Zwraca listę współrzędnych względnych dla danego wzoru.
    Można podać 'category/pattern' lub samo 'pattern' (sprawdza wszystkie kategorie)."""
    parts = name.split('/')
    if len(parts) == 2:
        category, pattern = parts
        return PATTERNS.get(category.lower(), {}).get(pattern.lower(), [])
    else:
        for category in PATTERNS.values():
            if name.lower() in category:
                return category[name.lower()]
        return []

def list_patterns() -> dict[str, list[str]]:
    """Zwraca słownik kategorii z listami wzorów."""
    return {cat: list(patterns.keys()) for cat, patterns in PATTERNS.items()}

def list_all_patterns() -> list[str]:
    """Zwracalistę wszystkich wzorów w formacie 'category/pattern'."""
    all_patterns = []
    for cat, patterns in PATTERNS.items():
        for pat in patterns:
            all_patterns.append(f"{cat}/{pat}")
    return all_patterns