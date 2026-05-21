"""Moduł definiujący proste struktury danych dla elementów graficznych (widoków)."""

import pygame

from dataclasses import dataclass

from gameoflife import config


@dataclass
class ViewRect:
    """Reprezentacja prostokąta z ramką."""
    x: int
    y: int
    width: int
    height: int

    color: tuple[int, int, int]
    border_color: tuple[int, int, int]
    border_radius: int


@dataclass
class ViewText:
    """Reprezentacja tekstu o określonym foncie i kolorze."""
    text: str
    x: int
    y: int
    
    color: tuple[int, int, int] = config.TEXT_COLOR
    font: str = "text_font"

    centered: bool = False


@dataclass
class ViewBackgroundColor:
    """Reprezentacja jednolitego tła ekranu."""
    color: tuple[int, int, int] = config.BACKGROUND_COLOR