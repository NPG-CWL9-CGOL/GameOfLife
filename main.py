import pygame
import random
from gameoflife.grid import Grid


# Ustawienia okna aplikacji
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Conway's Game of Life"


# Kolory
BACKGROUND_COLOR = (30, 30, 30)
GRID_BACKGROUND_COLOR = (40, 45, 55)
GRID_BORDER_COLOR = (100, 110, 125)
GRID_LINE_COLOR = (60, 65, 75)
ALIVE_CELL_COLOR = (120, 220, 130)
TEXT_COLOR = (230, 230, 230)
BOTTOM_PANEL_COLOR = (25, 25, 30)
BUTTON_COLOR = (55, 55, 65)
BUTTON_BORDER_COLOR = (120, 120, 130)


def draw_button(screen, x, y, width, height, text, font):
    """Rysuje prosty przycisk z tekstem."""
    pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, width, height), 2)

    button_text = font.render(text, True, TEXT_COLOR)
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(button_text, text_rect)


def draw_grid_outline(screen, grid_x, grid_y, grid_width, grid_height, cell_size):
    """
    Rysuje pustą planszę oraz kontury siatki.
    To realizuje zadanie: renderowanie konturu siatki.
    """
    pygame.draw.rect(
        screen,
        GRID_BACKGROUND_COLOR,
        (grid_x, grid_y, grid_width, grid_height)
    )

    # Linie pionowe
    for x in range(grid_x, grid_x + grid_width + 1, cell_size):
        pygame.draw.line(
            screen,
            GRID_LINE_COLOR,
            (x, grid_y),
            (x, grid_y + grid_height)
        )

    # Linie poziome
    for y in range(grid_y, grid_y + grid_height + 1, cell_size):
        pygame.draw.line(
            screen,
            GRID_LINE_COLOR,
            (grid_x, y),
            (grid_x + grid_width, y)
        )

    pygame.draw.rect(
        screen,
        GRID_BORDER_COLOR,
        (grid_x, grid_y, grid_width, grid_height),
        2
    )


def draw_cells(screen, grid, grid_x, grid_y, cell_size):
    """
    Rysuje żywe komórki na podstawie aktualnego stanu obiektu Grid.
    To realizuje zadanie: wizualizacja stanu komórek na siatce.
    """
    rows, cols = grid.shape

    for row in range(rows):
        for col in range(cols):
            if grid.data[row, col]:
                x = grid_x + col * cell_size
                y = grid_y + row * cell_size

                pygame.draw.rect(
                    screen,
                    ALIVE_CELL_COLOR,
                    (x + 2, y + 2, cell_size - 4, cell_size - 4)
                )


def fill_grid_randomly(grid, chance=0.2):
    """Losowo ustawia część komórek jako żywe, żeby było co wizualizować."""
    rows, cols = grid.shape

    for row in range(rows):
        for col in range(cols):
            if random.random() < chance:
                grid.set_cell(col, row, True)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont(None, 48)
    text_font = pygame.font.SysFont(None, 28)
    button_font = pygame.font.SysFont(None, 24)

    grid_x = 30
    grid_y = 90
    grid_width = 740
    grid_height = 380
    cell_size = 20

    cols = grid_width // cell_size
    rows = grid_height // cell_size

    grid_width = cols * cell_size
    grid_height = rows * cell_size

    grid = Grid(rows, cols)

    fill_grid_randomly(grid, chance=0.2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        title_text = title_font.render("Game of Life", True, TEXT_COLOR)
        screen.blit(title_text, (30, 25))

        draw_button(screen, 570, 25, 90, 35, "Projects", button_font)
        draw_button(screen, 670, 25, 90, 35, "Settings", button_font)

        draw_grid_outline(screen, grid_x, grid_y, grid_width, grid_height, cell_size)
        draw_cells(screen, grid, grid_x, grid_y, cell_size)

        pygame.draw.rect(screen, BOTTOM_PANEL_COLOR, (0, 500, WINDOW_WIDTH, 100))

        status_text = text_font.render("Status: Paused", True, TEXT_COLOR)
        screen.blit(status_text, (30, 515))

        draw_button(screen, 30, 550, 80, 35, "Start", button_font)
        draw_button(screen, 125, 550, 80, 35, "Stop", button_font)
        draw_button(screen, 220, 550, 80, 35, "Reset", button_font)
        draw_button(screen, 315, 550, 80, 35, "Step", button_font)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
