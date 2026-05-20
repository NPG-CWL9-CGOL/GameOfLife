from dataclasses import dataclass
import pygame

import gameoflife.config as config

from gameoflife.settings import AppSettings


@dataclass
class Button:
    """Klasa reprezentująca logikę guzika"""
    
    x: int
    y: int
    width: int
    height: int
    text: str
    font: pygame.font.Font

    color: tuple[int, int, int] = config.BUTTON_COLOR
    border_color: tuple[int, int, int] = config.BUTTON_COLOR
    text_color: tuple[int, int, int] = config.TEXT_COLOR

    def __post_init__(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # TODO: handle_event

