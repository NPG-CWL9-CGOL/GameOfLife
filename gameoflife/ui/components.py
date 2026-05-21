from __future__ import annotations

from abc import ABC

from gameoflife import config
from gameoflife.settings import AppSettings
from gameoflife.ui.views import ViewBackgroundColor, ViewRect, ViewText

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gameoflife.ui.core import UIState


class UIComponent(ABC):
    def __init__(self, ui_state: UIState):
        self.ui_state = ui_state

        self.layout_cached = None
        self.subcomponents_cached: dict[str, UIComponent] = None

    def get_layout(self):
        return []

    def get_subcomponents(self) -> dict[str, UIComponent]:
        return {}

    def get(self, name: str) -> UIComponent:
        if self.subcomponents_cached == None:
            return None
        
        return self.subcomponents_cached.get(name)

    def build_layout(self):
        self.layout_cached = self.get_layout()
        self.subcomponents_cached = self.get_subcomponents()

        for subcomponent in self.subcomponents_cached.values():
            subcomponent.build_layout()
            self.layout_cached.extend(subcomponent.get_layout())

    @property
    def views(self):
        return self.layout_cached

    def notify_changed(self):
        self.build_layout()


class EmptyComponent(UIComponent):
    def get_layout(self):
        return []


class QuickComponent(UIComponent):
    def __init__(self, view: any):
        super().__init__(None) # state for that case is None

        self.view = view

    def get_layout(self):
        return [ self.view ]


class Button(UIComponent):
    """Klasa reprezentująca komponent guzika"""

    color: tuple[int, int, int] = config.BUTTON_COLOR
    border_color: tuple[int, int, int] = config.BUTTON_BORDER_COLOR
    border_size: int = 2
    text_color: tuple[int, int, int] = config.TEXT_COLOR

    def __init__(
        self,
        ui_state: UIState,
        x: int, y: int,
        width: int, height: int,
        text: str,
        font: str = "button_font"
    ):
        super().__init__(ui_state)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

        self._click_handlers = []

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)

    def get_layout(self):
        return [
            ViewRect(
                self.x, self.y,
                self.width, self.height,
                self.color,
                self.border_color,
                self.border_size),
            ViewText(
                self.text,
                x=self.x + self.width / 2,
                y=self.y + self.height / 2,
                color=self.text_color,
                centered=True,
                font=self.font)
        ]

    def on_click(self, callback):
        """
        Dodanie funkcji odwołania na kliknięcie.
        Może być użyte jako dekorator.
        """
        if not callable(callback):
            raise TypeError("The delegate must be a callable function or method.")
        
        self._click_handlers.append(callback)
        return callback

    def click(self):
        for handler in self._click_handlers:
            handler()
    

class MainPage(UIComponent):
    def get_subcomponents(self):
        return {
            "settings_btn": Button(self.ui_state, 670, 25, 90, 35, "Settings"),
            "projects_btn": Button(self.ui_state, 570, 25, 90, 35, "Projects"),
            "start_btn":    Button(self.ui_state, 30, 550, 80, 35, "Start"),
            "stop_btn":     Button(self.ui_state, 125, 550, 80, 35, "Stop"),
            "reset_btn":    Button(self.ui_state, 220, 550, 80, 35, "Reset"),
            "step_btn":     Button(self.ui_state, 315, 550, 80, 35, "Step")
        }
    
    def get_layout(self):
        return [
            ViewText(
                text=f"Status: {'Editing' if self.ui_state.editing else 'Running'}",
                x=30, y=515),

            ViewText("Game of life", 30, 25, font="title_font")
        ]
    

class SettingsPage(UIComponent):
    def __init__(self, ui_state: UIState):
        super().__init__(ui_state)

    def get_subcomponents(self):
        return {
            "back_btn": Button(self.ui_state, 670, 25, 90, 35, "Back")
        }

    def get_layout(self):
        return [
            ViewText(
                text="Settings",
                x=30, y=25,
                font="title_font"),
            ViewRect(
                30, 90, 740, 380,
                color=config.GRID_BACKGROUND_COLOR,
                border_color=config.GRID_BORDER_COLOR,
                border_radius=2),
            *self.get_settings_views()
        ]


    def get_settings_views(self):
        settings = self.ui_state.settings
        settings_lines = [
            "Simulation:",
            f"Simulation speed: {settings.simulation_speed_ms} ms",
            f"Random fill chance: {settings.random_fill_chance}",
            f"Wrap edges: {settings.wrap_edges}",
            "",
            "Grid:",
            f"Grid size: {settings.grid_cols} x {settings.grid_rows}",
            f"Cell size: {settings.cell_size}",
            f"Show grid: {settings.show_grid}",
            "",
            "Editor:",
            f"Edit mode enabled: {settings.edit_mode_enabled}",
            f"Brush size: {settings.brush_size}",
            "",
            "Appearance:",
            f"Show FPS: {settings.show_fps}",
            f"Alive color: {settings.alive_color}",
            f"Dead color: {settings.dead_color}",
        ]

        for index, line in enumerate(settings_lines):
            yield ViewText(
                text=line,
                x=60,
                y=120 + index * 24
            )


class GlobalComponent(UIComponent):
    def __init__(self, ui_state: UIState):
        super().__init__(ui_state)

    def get_subcomponents(self):
        return {
            "main_title": QuickComponent(ViewBackgroundColor()),
            "main": MainPage(self.ui_state),
            "settings": SettingsPage(self.ui_state) 
        }