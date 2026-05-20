import pygame

from dataclasses import dataclass

import gameoflife.config as config

@dataclass
class ViewRect:
    x: int
    y: int
    width: int
    height: int

    color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    border_radius: int


@dataclass
class ViewText:
    text: set
    x: int
    y: int
    
    color: tuple[int, int, int] = config.TEXT_COLOR
    font: pygame.font.Font


@dataclass
class ViewBackgroundColor:
    color: tuple[int, int, int] = config.BACKGROUND_COLOR