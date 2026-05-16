import pygame
import random
from gameoflife.grid import Grid


#ustawienia okna aplikacji
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Conway's Game of Life"

# rysowanie przyciskow
def draw_button(screen, x, y, width, height, text, font):
    pygame.draw.rect(screen, (55, 55, 65), (x, y, width, height))
    pygame.draw.rect(screen, (120, 120, 130), (x, y, width, height), 2)
    button_text = font.render(text, True, (230, 230, 230))
    text_rect = button_text.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(button_text, text_rect)

def main():
    grid = Grid(100, 100)
    pygame.init()

    #okno aplikacji
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    #zegar fps
    clock = pygame.time.Clock()

    #czcionki
    title_font = pygame.font.SysFont(None, 48)
    text_font = pygame.font.SysFont(None, 28)
    button_font = pygame.font.SysFont(None, 24)

    # parametry obszaru symulacji
    grid_x = 30
    grid_y = 90
    grid_width = 740
    grid_height = 380
    cell_size = 20
    cols = grid_width // cell_size
    rows = grid_height // cell_size

    alive_cells = []

    for row in range(rows):
        for col in range(cols):
            if random.random() < 0.2:
                alive_cells.append((col, row))

    # glowna pętla programu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))
        title_text = title_font.render("Game of Life", True, (230, 230, 230))
        screen.blit(title_text, (30, 25))

        # przyciski nawigacji w górnej części okna
        draw_button(screen, 570, 25, 90, 35, "Projects", button_font)
        draw_button(screen, 670, 25, 90, 35, "Settings", button_font)

        pygame.draw.rect(screen, (40, 45, 55), (grid_x, grid_y, grid_width, grid_height))
        pygame.draw.rect(screen, (100, 110, 125), (grid_x, grid_y, grid_width, grid_height), 2)

        # rysowanie siatki i losowo zamalowanych komórek
        for row in range(rows):
            for col in range(cols):
                x = grid_x + col * cell_size
                y = grid_y + row * cell_size

                # obramowanie pojedynczej komórki
                pygame.draw.rect(screen, (60, 65, 75), (x, y, cell_size, cell_size), 1)

                # zamalowanie komórki, jeżeli znajduje się na liście alive_cells
                if (col, row) in alive_cells:
                    pygame.draw.rect(
                        screen,
                        (120, 220, 130),
                        (x + 2, y + 2, cell_size - 4, cell_size - 4)
                    )
        # dolny panel aplikacji
        pygame.draw.rect(screen, (25, 25, 30), (0, 500, WINDOW_WIDTH, 100))

        # status aplikacji
        status_text = text_font.render("Status: Paused", True, (230, 230, 230))
        screen.blit(status_text, (30, 515))

        # przyciski akcji
        draw_button(screen, 30, 550, 80, 35, "Start", button_font)
        draw_button(screen, 125, 550, 80, 35, "Stop", button_font)
        draw_button(screen, 220, 550, 80, 35, "Reset", button_font)
        draw_button(screen, 315, 550, 80, 35, "Step", button_font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
