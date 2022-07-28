import pygame
from labyrinth_algo import *
from guis import *

pygame.init()


def main():
    """Initializes and visualizes the labyrinth using pygame and the classes from labyrinth_algo.py.
    """

    # screen size and paddings
    top_pad = 50
    right_pad = 100
    screen_width = 900
    screen_height = 600

    # initialize screen object and pygame clock
    screen = pygame.display.set_mode((screen_width + right_pad, screen_height + top_pad))
    pygame.display.set_caption("Labyrinth Generator")
    clock = pygame.time.Clock()
    pygame.font.init()

    # Initialize font and labyrinth text info
    start_font = pygame.font.SysFont("arial", 40)
    lab_font = pygame.font.SysFont("sanscomic", 40)
    lab, grid_width, grid_height, block = None, None, None, None
    text_collection, buttons, save_button = lab_gui(lab_font, screen_width, screen_height, top_pad, right_pad,
                                                    Node.same_direction, Node.propagate_chance)

    # main loop of the game
    terminate = False
    grid_choice = False
    algo_choice = False
    part = 1

    while not terminate:
        clock.tick(15)

        # part 1 is the starting page where the user chooses the grid and the labyrinth generator
        if part == 1:

            # Gui to choose the grid size, at the start of the program or when reset
            if not grid_choice:

                grid = start_gui(screen, start_font, screen_width, top_pad, right_pad)  # looping till we choose

                if grid:
                    grid_width, grid_height = grid[0], grid[1]
                    block = screen_width // grid_width

                    screen.fill((80, 80, 80))
                    text_collection.draw(screen)
                    lab = Labyrinth(grid_width, grid_height, screen_width, screen_height, screen, block, top_pad)
                    lab.draw_grid()
                    pygame.display.flip()

                    grid_choice = True
                else:
                    terminate = True

            # when grid size is chosen we proceed to the lab gui
            if grid_choice:

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
                        if 0 <= x < grid_width and 0 <= y < grid_height:
                            """Here starts the path of the labyrinth"""
                            lab.path(x, y)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            lab.reset()
                            lab.draw_grid()
                            pygame.display.flip()

                        if event.key == pygame.K_r:
                            grid_choice = False

                        if event.key == pygame.K_s:
                            if not lab.empty:
                                part = 2

        # part 2 is the page where the user chooses the searching algorithm to use and then the search algo in the lab
        else:
            if not algo_choice:

                algo = search_choice_gui(screen, start_font, screen_width, top_pad, right_pad)

                if algo:
                    screen.fill((80, 80, 80))
                    lab.draw_grid()
                    lab.draw_tiles()
                    algo_choice = True
                    print("chosen")
                else:
                    terminate = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate = True

        pygame.display.flip()


if __name__ == "__main__":
    main()
