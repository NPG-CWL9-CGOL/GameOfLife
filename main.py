import pygame


#ustawienia okna aplikacji
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Conway's Game of Life"


def main():
    pygame.init()

    #okno aplikacji
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    #zegar fps
    clock = pygame.time.Clock()

    #napis
    font = pygame.font.SysFont(None, 64)
    title_text = font.render("Game of Life", True, (230, 230, 230))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))

    # glowna pętla programu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        screen.blit(title_text, title_rect)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
