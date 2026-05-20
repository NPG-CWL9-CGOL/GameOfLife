import pygame

import gameoflife.config as config

from gameoflife.grid import GridData

from gameoflife.ui.components import UIComponent
from gameoflife.ui.views import *

class GameRenderer:
    """Moduł odpowiedzialny za renderowanie obrazu"""
    
    def __init__(self, window_size: tuple[int, int], window_title: str) -> None:
        pygame.display.set_caption(window_title)
        self.screen = pygame.display.set_mode(window_size)

    def render():
        pass
