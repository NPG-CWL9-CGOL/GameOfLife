"""Główny moduł aplikacji łączący logikę, interfejs i renderowanie."""

from __future__ import annotations


import pygame

from gameoflife import config
from gameoflife.grid import GridData, GridGeometry, GridRenderer, fill_grid_randomly
from gameoflife.math_utils import point_in_rect
from gameoflife.settings import AppSettings
from gameoflife.ui.components import UIComponent
from gameoflife.ui.core import UIHandler, UIRenderer
from gameoflife.ui.views import *


class App:
    """Główna klasa zarządzająca cyklem życia aplikacji."""

    def __init__(
        self,
        renderer: AppRenderer,
        ui_handler: UIHandler,
        settings: AppSettings,
        grid_data: GridData,
        grid_geometry: GridGeometry
    ) -> None:
        """Inicjalizuje aplikację z niezbędnymi modułami i danymi."""
        self.renderer = renderer
        self.ui_handler = ui_handler
        self.settings = settings
        self.grid_data = grid_data
        self.grid_geometry = grid_geometry

        self.running = True

    @classmethod
    def create(cls) -> App:
        """Metoda fabryczna tworząca w pełni skonfigurowaną instancję aplikacji."""
        renderer = AppRenderer(
            window_size=(config.WINDOW_WIDTH, config.WINDOW_HEIGHT),
            window_title=config.WINDOW_TITLE)

        settings = AppSettings()

        grid_data, grid_geometry = App.create_grid(grid_x=30, grid_y=90)

        ui_handler = UIHandler(
            settings=settings,
            grid_data=grid_data,
            grid_geometry=grid_geometry
        )

        return cls(
            renderer, ui_handler, settings, grid_data, grid_geometry)


    def run(self) -> None:
        """Uruchamia główną pętlę aplikacji."""
        clock = pygame.time.Clock()
    
        while self.running:
            self.handle_events()
            self.renderer.render_begin()

            self.renderer.render_ui(
                self.ui_handler.get_active_components())

            if self.ui_handler.state.current_screen == "main":
                self.renderer.render_grid(
                    self.grid_data, self.grid_geometry)

            self.renderer.render_flush()

            clock.tick(config.FPS)


    def handle_events(self) -> None:
        """Przetwarza zdarzenia systemowe Pygame (mysz, klawiatura, wyjście)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.ui_handler.mouse_button_down(event)
            elif event.type == pygame.MOUSEMOTION:
                self.ui_handler.mouse_motion(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.ui_handler.mouse_button_up(event)


    @staticmethod
    def create_grid(grid_x: int, grid_y: int) -> tuple[GridData, GridGeometry]:
        """Tworzy i inicjalizuje strukturę danych siatki oraz jej geometrię."""
        grid_width = 740
        grid_height = 380
        cell_size = 20

        cols = grid_width // cell_size
        rows = grid_height // cell_size

        grid_width = cols * cell_size
        grid_height = rows * cell_size

        grid_data = GridData(rows, cols)
        grid_geometry = GridGeometry(
            grid_data=grid_data,
            x=grid_x, y=grid_y,
            width=grid_width, height=grid_height,
            cell_size=cell_size)
        

        fill_grid_randomly(grid_data, chance=0.2)

        return grid_data, grid_geometry



class AppRenderer:
    """Moduł odpowiedzialny za renderowanie obrazu"""
    
    def __init__(self, window_size: tuple[int, int], window_title: str) -> None:
        """Inicjalizuje okno graficzne i systemy renderowania składowych."""
        self.window_size = window_size
        
        pygame.init()

        pygame.display.set_caption(window_title)
        self.screen = pygame.display.set_mode(window_size)
        
        self.grid_renderer = GridRenderer(self.screen)
        self.ui_renderer = UIRenderer(self.screen)

        
    def __del__(self) -> None:
        """Zamyka system Pygame przy usuwaniu obiektu."""
        pygame.quit()
 

    def render_begin(self) -> None:
        """Przygotowuje klatkę do renderowania (rysuje panel)."""
        pygame.draw.rect(self.screen, config.BOTTOM_PANEL_COLOR, (0, 500, self.window_size[0], 100))


    def render_grid(self, grid_data: GridData, grid_geometry: GridGeometry) -> None:                
        """Rysuje siatkę symulacji wraz z jej komórkami."""
        self.grid_renderer.render_outline(grid_geometry)
        self.grid_renderer.render_cells(grid_data, grid_geometry)


    def render_ui(self, components: list[UIComponent]) -> None:
        """Renderuje listę aktywnych komponentów interfejsu."""
        for component in components:
            self.ui_renderer.render_component(component)

    def render_flush(self) -> None:
        """Odświeżanie ekranu"""
        pygame.display.flip()
    
