from abc import ABC, abstractmethod

import pygame

import gameoflife.config as config
from gameoflife.settings import AppSettings
from gameoflife.ui.views import ViewRect, ViewText


class UIComponent(ABC):
    def __init__(self):
        self._subcomponents: list[UIComponent] = []
        self._layout = None

    @abstractmethod
    def get_layout(self):
        pass

    def build_layout(self):
        self._layout = self.get_layout()

        for subcomponent in self._subcomponents:
            self._layout.extend(subcomponent.get_layout())

    @property
    def views(self):
        return self._layout


class Button(UIComponent):
    """Klasa reprezentująca komponent guzika"""

    color: tuple[int, int, int] = config.BUTTON_COLOR
    border_color: tuple[int, int, int] = config.BUTTON_COLOR
    border_size: int = 2
    text_color: tuple[int, int, int] = config.TEXT_COLOR

    def __init__(
        self,
        x: int, y: int,
        width: int, height: int,
        text: str,
        font: pygame.font.Font = pygame.font.SysFont(None, 24)
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

        super().__init__()

    def get_layout(self):
        self._layout = [
            ViewRect(
                self.x, self.y,
                self.width, self.height,
                self.text, self.font,
                self.color,
                self.border_color,
                self.border_size),
            ViewText(
                self.text,
                x=self.x + self.width / 2,
                y=self.y + self.height / 2,
                color=self.text_color)
        ]


class SettingsPanel(UIComponent):    
    title_font = pygame.font.SysFont(None, 48)
    text_font = pygame.font.SysFont(None, 28)
    button_font = pygame.font.SysFont(None, 24)

    def __init__(self, settings: AppSettings):
        super().__init__()
        self.settings = settings

        self._subcomponents.extend([
            Button(
                670, 25, 90, 35,
                "Back",)
        ])

    def get_layout(self):
        return [
            ViewText(
                text="Settings",
                x=30, y=25),
            ViewRect(
                30, 90, 740, 380,
                color=config.GRID_BACKGROUND_COLOR,
                border_color=config.GRID_BORDER_COLOR,
                border_radius=2)
        ].extend(self.get_settings_components())


    def get_settings_components(self):
        settings_lines = [
            "Simulation:",
            f"Simulation speed: {self.settings.simulation_speed_ms} ms",
            f"Random fill chance: {self.settings.random_fill_chance}",
            f"Wrap edges: {self.settings.wrap_edges}",
            "",
            "Grid:",
            f"Grid size: {self.settings.grid_cols} x {self.settings.grid_rows}",
            f"Cell size: {self.settings.cell_size}",
            f"Show grid: {self.settings.show_grid}",
            "",
            "Editor:",
            f"Edit mode enabled: {self.settings.edit_mode_enabled}",
            f"Brush size: {self.settings.brush_size}",
            "",
            "Appearance:",
            f"Show FPS: {self.settings.show_fps}",
            f"Alive color: {self.settings.alive_color}",
            f"Dead color: {self.settings.dead_color}",
        ]

        for index, line in enumerate(settings_lines):
            yield ViewText(
                text=line,
                x=60,
                y=120 + index * 24
            )