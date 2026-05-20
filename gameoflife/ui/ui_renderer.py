import pygame

from gameoflife.ui.components import UIComponent
from gameoflife.ui.views import *

class UIRenderer:
    def __init__(self, screen):
        self.screen = screen

        self._render_dispatch = {
            ViewRect: self._render_rect,
            ViewText: self._render_text,
            ViewBackgroundColor: self._render_background
        }

    def render_component(self, component: UIComponent):
        for view in component.views():
            render_method = self._render_dispatch.get(type(view))
            
            if render_method:
                render_method(view)
            else:
                print(f"Warning: No rendering method registered for {type(view)}")


    def _render_rect(self, rect_view: ViewRect):
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


    def _render_text(self, text_view: ViewText):
        text = text_view.font.render(
            text_view.text, True, text_view.text_color)
        
        text_rect = text.get_rect(
            center=(text_view.x, text_view.y))
        
        self.screen.blit(text, text_rect)


    def _render_background(self, bg_view: ViewBackgroundColor):
        self.screen.fill(bg_view.color)

