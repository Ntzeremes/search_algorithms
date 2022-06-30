import pygame
from labyrinth_algo import *
from guis import *

pygame.init()


def main():
    """Initializes and visualizes the labyrinth using pygame and the classes from labyrinth_algo.py.
    """

    # pygame
    top_pad = 50
    right_pad = 100
    screen_width = 900
    screen_height = 600
    screen = pygame.display.set_mode((screen_width + right_pad, screen_height + top_pad))
    pygame.display.set_caption("Labyrinth Generator")
    clock = pygame.time.Clock()
    pygame.font.init()

    # Initialize font and labyrinth text info
    start_font = pygame.font.SysFont("arial", 40)
    lab_font = pygame.font.SysFont("sanscomic", 40)
    lab, width, height, block = None, None, None, None
    text_collection, buttons, save_button = lab_gui(lab_font, screen_width, screen_height, top_pad, right_pad,
                                       Node.same_direction, Node.propagate_chance)
    terminate = False

    start_settings = False
    while not terminate:
        clock.tick(60)

        if lab:
            text_collection.draw(screen)
            buttons.draw(screen)
            save_button.draw(screen)
            buttons.ckeck_click()
            save_button.check_click(lab)

        if start_settings:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = int((event.pos[0]) // block)
                    y = int((event.pos[1] - top_pad) // block)
                    if 0 <= x < width and 0 <= y < height:
                        lab.path(x, y)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        lab.reset()
                        draw_grid(screen, screen_width, screen_height, width, height, top_pad)
                        pygame.display.flip()

                    if event.key == pygame.K_r:
                        start_settings = False

        # Gui to choose the grid size, at the start of the program or when reset
        if not start_settings:
            grid_choice = starting_gui(screen, start_font, screen_width, top_pad, right_pad)  # looping till we choose

            # If we decided to close the settings we get no choice , so we need an if clause to check this
            if grid_choice:
                width, height = grid_choice[0], grid_choice[1]
                screen.fill((80, 80, 80))
                lab = Labyrinth(width, height)
                block = screen_width // width
                lab.set_visual_p(screen, block, top_pad)
                draw_grid(screen, screen_width, screen_height, width, height, top_pad)
                pygame.display.flip()
                start_settings = True
            else:
                terminate = True

        pygame.display.flip()


if __name__ == "__main__":
    main()