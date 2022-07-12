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
    lab_width = 900
    lab_height = 600
    screen = pygame.display.set_mode((lab_width + right_pad, lab_height + top_pad))
    pygame.display.set_caption("Labyrinth Generator")
    clock = pygame.time.Clock()
    pygame.font.init()

    # Initialize font and labyrinth text info
    start_font = pygame.font.SysFont("arial", 40)
    lab_font = pygame.font.SysFont("sanscomic", 40)
    lab, width, height, block = None, None, None, None
    text_collection, buttons, save_button = lab_gui(lab_font, lab_width, lab_height, top_pad, right_pad,
                                       Node.same_direction, Node.propagate_chance)

    # main loop of the game

    terminate = False
    start_settings = False
    page = 1
    while not terminate:
        clock.tick(10)

        # Gui to choose the grid size, at the start of the program or when reset
        if not start_settings:
            # page 1 is the starting page where the user chooses the grid
            if page == 1:
                grid_choice = starting_gui(screen, start_font, lab_width, top_pad, right_pad)  # looping till we choose

                # If we decided to close the settings we get no choice. So we need an if clause to check this and
                # terminate the game in case of sucH an event

                if grid_choice:
                    width, height = grid_choice[0], grid_choice[1]
                    screen.fill((80, 80, 80))
                    lab = Labyrinth(width, height)
                    block = lab_width // width
                    lab.set_visual_p(screen, block, top_pad)
                    draw_grid(screen, lab_width, lab_height, width, height, top_pad)
                    pygame.display.flip()
                    start_settings = True
                else:
                    terminate = True
            # page 2 is the page where the user chooses the searching algorithm to use.
            else:
                algo = search_gui(screen, start_font, lab_width, top_pad, right_pad)
                print(algo)
                start_settings = True

        if start_settings:

            text_collection.draw(screen)
            buttons.draw(screen)
            save_button.draw(screen)
            buttons.ckeck_click()
            save_button.check_click(lab)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = int((event.pos[0]) // block)
                    y = int((event.pos[1] - top_pad) // block)
                    if 0 <= x < width and 0 <= y < height:
                        print(x, y)
                        lab.path(x, y)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        lab.reset()
                        draw_grid(screen, lab_width, lab_height, width, height, top_pad)
                        pygame.display.flip()

                    if event.key == pygame.K_r:
                        start_settings = False

                    if event.key == pygame.K_s:
                        if not lab.empty:
                            page = 2
                            start_settings = False

        pygame.display.flip()


if __name__ == "__main__":
    main()