from gameoflife.grid import GridData, GridGeometry
from gameoflife.settings import AppSettings

import pygame

from gameoflife.math_utils import point_in_rect
from gameoflife.ui.components import GlobalComponent, UIComponent
from gameoflife.ui.views import *


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
    drag_target_state: tuple[int, int] = None
    drag_previous_cell: tuple[int, int] = None
    current_screen: str = "main"


class UIHandler:
    def __init__(self, settings: AppSettings, grid_data: GridData, grid_geometry: GridGeometry):
        self.state = UIState(settings=settings)

        self.grid_data = grid_data  
        self.grid_geometry = grid_geometry

        self.global_component = GlobalComponent(self.state)
        self.global_component.build_layout()

        self.back_btn = (
            self.global_component
                .get("settings")
                .get("back_btn")
        )

        self.settings_btn = (
            self.global_component
                .get("main")
                .get("settings_btn")
        )

        @self.back_btn.on_click
        def _():
            self.state.current_screen = "main"


        @self.settings_btn.on_click
        def _():
            self.state.current_screen = "settings"
            self.state.drag_target_state = None
            self.state.drag_previous_cell = None



    def get_active_components(self):
        return [
            self.global_component.get("main_title"),
            self.global_component.get(self.state.current_screen)
        ]


    def mouse_button_down(self, event):
        if event.button != 1:
            return
        
        if self.state.current_screen == "settings":
            if point_in_rect(event.pos, self.back_btn.get_rect()):
                self.back_btn.click()
            
        elif point_in_rect(event.pos, self.settings_btn.get_rect()):
            self.settings_btn.click()
            
        else:
            self.state.drag_target_state, self.state.drag_previous_cell = self.handle_grid_click(event)


    def mouse_motion(self, event):
        if self.state.current_screen != "main" or self.state.drag_target_state is None:
            return
        
        self.state.drag_previous_cell = self.continue_grid_drag(event)
    

    def mouse_button_up(self, event):
        if event.button != 1:
            return
        
        self.state.drag_target_state = None
        self.state.drag_previous_cell = None


    def handle_grid_click(self, event):
        """Obsługa kliknięcia w siatkę, z pominięciem obszarów UI.
        Zwraca stan pędzla dla przeciągania komórek."""
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

        
    #to reaguje na mousemotion, wazne w nowej petli zdarzen 
    def continue_grid_drag(self, event):
        """Obsługa przeciągania myszy po siatce w trakcie edycji."""

        if not self.state.editing or self.state.drag_target_state is None or self.state.drag_previous_cell is None:
            return self.state.drag_previous_cell

        if any(point_in_rect(event.pos, rect) for rect in UI_RECTS):
            return self.state.drag_previous_cell

        cell = self.grid_geometry.get_cell(event.pos)
        if cell is None:
            return self.state.drag_previous_cell

        if cell != self.state.drag_previous_cell:
            self.grid_geometry.draw_line(self.state.drag_previous_cell, cell, self.state.drag_target_state)
        
        return cell




class UIRenderer:
    def __init__(self, screen):
        self.screen = screen

        self._render_dispatch = {
            ViewRect:               self.render_rect,
            ViewText:               self.render_text,
            ViewBackgroundColor:    self.render_background
        }


        self.fonts = {
            "title_font": pygame.font.SysFont(None, 48),
            "text_font": pygame.font.SysFont(None, 28),
            "button_font": pygame.font.SysFont(None, 24)
        }


    def render_component(self, component: UIComponent):
        for view in component.views:
            render_method = self._render_dispatch.get(type(view))
            
            if render_method:
                render_method(view)
            else:
                print(f"Warning: No rendering method registered for {type(view)}")


    def render_rect(self, rect_view: ViewRect):
        rect = pygame.Rect(
            rect_view.x,
            rect_view.y,
            rect_view.width,
            rect_view.height)
            
        pygame.draw.rect(
            self.screen, rect_view.color, rect)
        
        pygame.draw.rect(
            self.screen,
            rect_view.border_color,
            rect,
            rect_view.border_radius)


    def render_text(self, text_view: ViewText):
        text = self.fonts[text_view.font].render(
            text_view.text, True, text_view.color)
        
        if text_view.centered:
            text_rect = text.get_rect(
                center=(text_view.x, text_view.y))
            self.screen.blit(text, text_rect)
        else:
            self.screen.blit(text, (text_view.x, text_view.y))


    def render_background(self, bg_view: ViewBackgroundColor):
        self.screen.fill(bg_view.color)
