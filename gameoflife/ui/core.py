"""Rdzeń systemu interfejsu użytkownika, obsługujący stan i logikę zdarzeń."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from gameoflife.engine import Engine
from gameoflife.grid import GridData, GridGeometry
from gameoflife.math_utils import point_in_rect
from gameoflife.settings import AppSettings
from gameoflife.ui.components import GlobalComponent, UIComponent
from gameoflife.ui.views import ViewBackgroundColor, ViewRect, ViewText


# TODO: dynamic component boundaries
UI_RECTS = [
    (570, 25, 90, 35),
    (670, 25, 90, 35),
    (30, 550, 80, 35),
    (125, 550, 80, 35),
    (220, 550, 80, 35),
    (315, 550, 80, 35)
]


@dataclass
class UIState:

    settings: AppSettings

    editing: bool = True
    drag_target_state: bool | None = None
    drag_previous_cell: tuple[int, int] | None = None
    current_screen: str = "main"


class UIHandler:

    def __init__(
        self,
        settings: AppSettings,
        grid_data: GridData,
        grid_geometry: GridGeometry
    ):
        self.state = UIState(settings=settings)

        self.grid_data = grid_data
        self.grid_geometry = grid_geometry
        self.engine = Engine(grid_data)

        self.last_simulation_update_ms = pygame.time.get_ticks()

        self.global_component = GlobalComponent(self.state)
        self.global_component.build_layout()

        self.main_page = self.global_component.get("main")
        self.settings_page = self.global_component.get("settings")

        self.back_btn = self.settings_page.get("back_btn")
        self.settings_btn = self.main_page.get("settings_btn")

        self.start_btn = self.main_page.get("start_btn")
        self.stop_btn = self.main_page.get("stop_btn")
        self.reset_btn = self.main_page.get("reset_btn")
        self.step_btn = self.main_page.get("step_btn")

        self._connect_buttons()

    def _connect_buttons(self) -> None:

        @self.back_btn.on_click
        def _():
            self.state.current_screen = "main"
            self._stop_dragging()

        @self.settings_btn.on_click
        def _():
            self.state.current_screen = "settings"
            self._stop_dragging()

        @self.start_btn.on_click
        def _():
            self.state.editing = False
            self.last_simulation_update_ms = pygame.time.get_ticks()
            self._stop_dragging()
            self._refresh_main_page()

        @self.stop_btn.on_click
        def _():
            self.state.editing = True
            self._stop_dragging()
            self._refresh_main_page()

        @self.reset_btn.on_click
        def _():
            self.grid_data.reset_grid()
            self.state.editing = True
            self._stop_dragging()
            self._refresh_main_page()

        @self.step_btn.on_click
        def _():
            self.engine.update()
            self._stop_dragging()

    def _refresh_main_page(self) -> None:
        self.main_page.notify_changed()

    def _stop_dragging(self) -> None:
        self.state.drag_target_state = None
        self.state.drag_previous_cell = None

    def update_simulation(self) -> None:
        if self.state.current_screen != "main":
            return

        if self.state.editing:
            return

        now_ms = pygame.time.get_ticks()
        interval_ms = self.state.settings.simulation_speed_ms

        if now_ms - self.last_simulation_update_ms >= interval_ms:
            self.engine.update()
            self.last_simulation_update_ms = now_ms

    def get_active_components(self) -> list[UIComponent]:
        return [
            self.global_component.get("main_title"),
            self.global_component.get(self.state.current_screen)
        ]

    def mouse_button_down(self, event: pygame.event.Event) -> None:
        if event.button != 1:
            return

        if self.state.current_screen == "settings":
            if point_in_rect(event.pos, self.back_btn.get_rect()):
                self.back_btn.click()
            return

        if point_in_rect(event.pos, self.settings_btn.get_rect()):
            self.settings_btn.click()
            return

        if point_in_rect(event.pos, self.start_btn.get_rect()):
            self.start_btn.click()
            return

        if point_in_rect(event.pos, self.stop_btn.get_rect()):
            self.stop_btn.click()
            return

        if point_in_rect(event.pos, self.reset_btn.get_rect()):
            self.reset_btn.click()
            return

        if point_in_rect(event.pos, self.step_btn.get_rect()):
            self.step_btn.click()
            return

        self.state.drag_target_state, self.state.drag_previous_cell = (
            self.handle_grid_click(event)
        )

    def mouse_motion(self, event: pygame.event.Event) -> None:
        if self.state.current_screen != "main":
            return

        if self.state.drag_target_state is None:
            return

        self.state.drag_previous_cell = self.continue_grid_drag(event)

    def mouse_button_up(self, event: pygame.event.Event) -> None:
        if event.button != 1:
            return

        self._stop_dragging()

    def handle_grid_click(
        self,
        event: pygame.event.Event
    ) -> tuple[bool | None, tuple[int, int] | None]:
        if self.state.editing is False:
            return None, None

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None, None

        if any(point_in_rect(event.pos, rect) for rect in UI_RECTS):
            return None, None

        cell = self.grid_geometry.get_cell(event.pos)

        if cell is None:
            return None, None

        col, row = cell
        current_state = self.grid_data.get_cell(col, row)
        target_state = not current_state

        self.grid_geometry.draw_line(cell, cell, target_state)

        return target_state, cell

    def continue_grid_drag(self, event: pygame.event.Event) -> tuple[int, int] | None:
        if not self.state.editing:
            return self.state.drag_previous_cell

        if self.state.drag_target_state is None:
            return self.state.drag_previous_cell

        if self.state.drag_previous_cell is None:
            return self.state.drag_previous_cell

        if any(point_in_rect(event.pos, rect) for rect in UI_RECTS):
            return self.state.drag_previous_cell

        cell = self.grid_geometry.get_cell(event.pos)

        if cell is None:
            return self.state.drag_previous_cell

        if cell != self.state.drag_previous_cell:
            self.grid_geometry.draw_line(
                self.state.drag_previous_cell,
                cell,
                self.state.drag_target_state
            )

        return cell


class UIRenderer:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self._render_dispatch = {
            ViewRect: self.render_rect,
            ViewText: self.render_text,
            ViewBackgroundColor: self.render_background
        }

        self.fonts = {
            "title_font": pygame.font.SysFont(None, 48),
            "text_font": pygame.font.SysFont(None, 28),
            "button_font": pygame.font.SysFont(None, 24)
        }

    def render_component(self, component: UIComponent) -> None:
        for view in component.views:
            render_method = self._render_dispatch.get(type(view))

            if render_method:
                render_method(view)
            else:
                print(f"Warning: No rendering method registered for {type(view)}")

    def render_rect(self, rect_view: ViewRect) -> None:
        rect = pygame.Rect(
            rect_view.x,
            rect_view.y,
            rect_view.width,
            rect_view.height
        )

        pygame.draw.rect(
            self.screen,
            rect_view.color,
            rect
        )

        pygame.draw.rect(
            self.screen,
            rect_view.border_color,
            rect,
            rect_view.border_radius
        )

    def render_text(self, text_view: ViewText) -> None:
        text = self.fonts[text_view.font].render(
            text_view.text,
            True,
            text_view.color
        )

        if text_view.centered:
            text_rect = text.get_rect(
                center=(text_view.x, text_view.y)
            )
            self.screen.blit(text, text_rect)
        else:
            self.screen.blit(text, (text_view.x, text_view.y))

    def render_background(self, bg_view: ViewBackgroundColor) -> None:
        self.screen.fill(bg_view.color)