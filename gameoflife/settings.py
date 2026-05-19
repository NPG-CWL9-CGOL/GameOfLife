from dataclasses import dataclass


@dataclass
class AppSettings:
# Model ustawien aplikacji

    cell_size: int = 20
    random_fill_chance: float = 0.2
    simulation_speed_ms: int = 200
    show_grid: bool = True
    wrap_edges: bool = True
    alive_color: tuple[int, int, int] = (120, 220, 130)
    dead_color: tuple[int, int, int] = (40, 45, 55)