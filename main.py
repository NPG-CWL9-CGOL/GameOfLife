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


def point_in_rect(pos, rect) -> bool:
    """Sprawdza, czy punkt (x, y) znajduje się w prostokącie."""
    x, y = pos
    rx, ry, rw, rh = rect
    return rx <= x < rx + rw and ry <= y < ry + rh

#zamiana wspolrzednych myszy na indeksy komorek w siatce
def get_grid_cell(pos, grid_x, grid_y, grid_width, grid_height, cell_size):
    mx, my = pos
    if not (grid_x <= mx < grid_x + grid_width and grid_y <= my < grid_y + grid_height):
        return None

    col = (mx - grid_x) // cell_size
    row = (my - grid_y) // cell_size
    return col, row


def draw_line_on_grid(grid, start_cell, end_cell, state):
    """Rysuje linię komórek między dwoma punktami na siatce."""
    x0, y0 = start_cell
    x1, y1 = end_cell
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        grid.set_cell(x0, y0, state)
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

#teraz zwracamy stan pędzla zamiast togglowania pojedynczej komorki
def handle_grid_click(event, grid, grid_x, grid_y, grid_width, grid_height, cell_size, ui_rects, editing):
    """Obsługa kliknięcia w siatkę, z pominięciem obszarów UI.
    Zwraca stan pędzla dla przeciągania komórek."""
    if editing is False:
        return None, None

    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return None, None

    if any(point_in_rect(event.pos, rect) for rect in ui_rects):
        return None, None

    cell = get_grid_cell(event.pos, grid_x, grid_y, grid_width, grid_height, cell_size)
    if cell is None:
        return None, None

    col, row = cell
    current_state = grid.get_cell(col, row)
    target_state = not current_state
    draw_line_on_grid(grid, cell, cell, target_state)
    return target_state, cell

#to reaguje na mousemotion, wazne w nowej petli zdarzen 
def continue_grid_drag(event, grid, grid_x, grid_y, grid_width, grid_height, cell_size, ui_rects, editing, target_state, previous_cell):
    """Obsługa przeciągania myszy po siatce w trakcie edycji."""
    if editing is False or target_state is None or previous_cell is None:
        return previous_cell

    if any(point_in_rect(event.pos, rect) for rect in ui_rects):
        return previous_cell

    cell = get_grid_cell(event.pos, grid_x, grid_y, grid_width, grid_height, cell_size)
    if cell is None:
        return previous_cell

    if cell != previous_cell:
        draw_line_on_grid(grid, previous_cell, cell, target_state)
    return cell


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

    ui_rects = [
        (570, 25, 90, 35),
        (670, 25, 90, 35),
        (30, 550, 80, 35),
        (125, 550, 80, 35),
        (220, 550, 80, 35),
        (315, 550, 80, 35)
    ]

    editing = True
    drag_target_state = None
    drag_previous_cell = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drag_target_state, drag_previous_cell = handle_grid_click(
                    event,
                    grid,
                    grid_x,
                    grid_y,
                    grid_width,
                    grid_height,
                    cell_size,
                    ui_rects,
                    editing
                )
            elif event.type == pygame.MOUSEMOTION and drag_target_state is not None:
                drag_previous_cell = continue_grid_drag(
                    event,
                    grid,
                    grid_x,
                    grid_y,
                    grid_width,
                    grid_height,
                    cell_size,
                    ui_rects,
                    editing,
                    drag_target_state,
                    drag_previous_cell
                )
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drag_target_state = None
                drag_previous_cell = None

        screen.fill(BACKGROUND_COLOR)

        title_text = title_font.render("Game of Life", True, TEXT_COLOR)
        screen.blit(title_text, (30, 25))

        draw_button(screen, 570, 25, 90, 35, "Projects", button_font)
        draw_button(screen, 670, 25, 90, 35, "Settings", button_font)

        draw_grid_outline(screen, grid_x, grid_y, grid_width, grid_height, cell_size)
        draw_cells(screen, grid, grid_x, grid_y, cell_size)

        pygame.draw.rect(screen, BOTTOM_PANEL_COLOR, (0, 500, WINDOW_WIDTH, 100))

        status_text = text_font.render(
            f"Status: {'Editing' if editing else 'Running'}",
            True,
            TEXT_COLOR
        )
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
