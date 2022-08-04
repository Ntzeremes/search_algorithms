import csv
import pygame
from labyrinth_algo import Node


class Text:
    """Text class that created and prints text on the screen surface"""

    def __init__(self, font, pos, width, height, text, text_color=(255, 255, 255), top_color=(0, 0, 0)):
        self.font = font
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color
        self.text = text
        self.text_color = text_color

        self.text_surf = font.render(text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        screen.blit(self.text_surf, self.text_rect)


class Changing_Text(Text):
    """Child class of Text, used when we want to have a text that changes."""
    def change_text(self, value):
        self.text = f"{self.text[0]}:{value}"


class Text_Collection:
    """Collection of text objects so that with one draw call, all texts in the collection can be drawn"""

    def __init__(self, texts):
        self.texts = texts

    def draw(self, screen):
        for text in self.texts:
            text.draw(screen)


class Button:
    """Creates the buttons for gui"""

    def __init__(self, text, width, height, pos, font, changing_text=None):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (160, 160, 160)
        self.pressed = False
        self.changing_text = changing_text
        self.text = text

        self.text_surf = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(*mouse_pos):
            self.top_color = (220, 220, 220)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    if self.changing_text:
                        if self.changing_text.text[0] == "p":
                            self.changing_text.change_text(Node.change_propagate(self.text))
                        else:
                            self.changing_text.change_text(Node.change_direction(self.text))
                    self.pressed = False
                    return True
        else:
            self.top_color = (160, 160, 160)
        return False


class Image_Button:
    """Special Button class used for the save icon"""
    def __init__(self, x, y, image, width, height):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.top_rect = pygame.Rect((x, y), (50, 50))
        self.pressed = False
        self.screen_width = width
        self.screen_height = height

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_click(self, lab):
        """If clicked the save button saves the pygame screen as a png and the labyrinth grid inside a txt file"""
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    with open("labyrinth.txt", "w") as f:
                        writer = csv.writer(f)
                        writer.writerows(lab.grid)

                    self.save_image(self.screen_width, self.screen_height, lab)
                    self.pressed = False
                    return True
        else:
            pass
        return False

    def save_image(self, screen_width, screen_height, lab):
        """Function that uses pillow to save the labyrinth tiles as a png file."""
        from PIL import Image, ImageDraw

        grid = lab.grid
        height = len(grid)
        width = len(grid[0])

        block = screen_width // width

        img = Image.new("RGBA", (screen_width, screen_height), "black")
        cell_border = 2
        draw = ImageDraw.Draw(img)

        for i in range(height):
            for j in range(width):
                # path
                if grid[i][j] == 0:
                    fill = (175, 175, 175)
                # walls
                else:
                    fill = (80, 80, 80)

                # Draw cell
                draw.rectangle([(j * block + cell_border, i * block + cell_border),
                                ((j + 1) * block - cell_border, (i + 1) * block - cell_border)], fill=fill
                               )

        img.save("labyrinth.png")


class Button_Collection:
    def __init__(self, buttons):
        self.buttons = buttons

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def ckeck_click(self):
        for button in self.buttons:
            button.check_click()


# noinspection PyUnresolvedReferences
def start_gui(screen, font, width, top_pad, right_pad):
    """Creating the starting screen from which the user will choose the size of the labyrinth.

    Returns the grid size chosen by the user."""

    terminate = False
    clock = pygame.time.Clock()

    # possible choices
    choice = None
    grid_choices = {0: [None, "9 x 6", (9, 6)], 1: [None, "15 x 10", (15, 10)], 2: [None, "30 x 20", (30, 20)],
                    3: [None, "60 x 40", (60, 40)]}
    text = "Choose the labyrinth grid size."
    page_text = Text(font, (100, 100), width - right_pad, 40, text)
    button_h = 90

    for i in range(len(grid_choices)):
        # noinspection PyTypeChecker
        grid_choices[i][0] = Button(grid_choices[i][1], 200, 50, (400, 210 + i * button_h), font)

    screen.fill((0, 0, 0))
    page_text.draw(screen)

    while not terminate:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

        for i in range(len(grid_choices)):
            grid_choices[i][0].draw(screen)
            if grid_choices[i][0].check_click():
                choice = grid_choices[i][2]
                terminate = True

        pygame.display.flip()

    return choice


def lab_gui(font, width, height, top_pad, right_pad, d, p):
    """Creates the lab gui that has some text that guides the user and some buttons to change
    the labyrinth parameters"""
    # TEXT
    button_font = pygame.font.SysFont("arial", 40)
    title_font = pygame.font.SysFont("arial", 50)
    title_text = "Creating labyrinth"
    horizontal_text = "Space: clear labyrinth    R : reset the grid size    S :  search algo"
    h_text = Text(font, (90, 60), width - 2 * right_pad, 50, horizontal_text, (0, 0, 0), (80, 80, 80))
    t_text = Text(title_font, (90, 0), width - 2 * right_pad, 70, title_text, (0, 0, 0), (80, 80, 80))

    # d text and buttons
    vertical_text1 = f"d:{d}"
    v_text1 = Changing_Text(font, (width + 2, 1.5 * top_pad), right_pad, 50, vertical_text1, (0, 0, 0), (80, 80, 80))
    d_plus = Button("+", right_pad / 2 - 10, right_pad / 2 - 10, (width + 5 + right_pad / 4, 1.5 * top_pad - 50),
                    button_font,
                    v_text1)
    d_minus = Button("-", right_pad / 2 - 10, right_pad / 2 - 10, (width + 5 + right_pad / 4, 1.5 * top_pad + 50),
                     button_font,
                     v_text1)

    # p text and buttons
    vertical_text2 = f"p:{p}"
    v_text2 = Changing_Text(font, (width + 2, 3.5 * top_pad), right_pad, 50, vertical_text2, (0, 0, 0), (80, 80, 80))
    p_plus = Button("+", right_pad / 2 - 10, right_pad / 2 - 10, (width + 5 + right_pad / 4, 3.5 * top_pad - 50),
                    button_font,
                    v_text2)
    p_minus = Button("-", right_pad / 2 - 10, right_pad / 2 - 10, (width + 5 + right_pad / 4, 3.5 * top_pad + 50),
                     button_font,
                     v_text2)

    # save image
    save_image = pygame.image.load("save.png").convert_alpha()
    save_image = pygame.transform.scale(save_image, (50, 50))
    save_button = Image_Button(width + right_pad / 4, 5 * top_pad, save_image, width, height)

    # group buttons and text
    buttons = Button_Collection([d_plus, d_minus, p_minus, p_plus])
    collection = Text_Collection([h_text, v_text1, v_text2, t_text])
    return collection, buttons, save_button


def search_choice_gui(screen, font, width, top_pad, right_pad):
    """Creating the gui from which the user will choose a search algorithm

    Returns the choice"""

    terminate = False
    clock = pygame.time.Clock()

    choice = None
    grid_choices = {0: [None, "Breadth first", 1], 1: [None, "Depth First", 2], 2: [None, "A*", 3],
                    3: [None, "b", 4]}
    text = "Choose search algorithm."
    page_text = Text(font, (100, 100), width - right_pad, 40, text)
    button_h = 90

    for i, _ in enumerate(grid_choices):
        # noinspection PyTypeChecker
        grid_choices[i][0] = Button(grid_choices[i][1], 240, 50, (380, 210 + i * button_h), font)

    while not terminate:
        screen.fill((0, 0, 0))
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

        page_text.draw(screen)

        for i, _ in enumerate(grid_choices):
            grid_choices[i][0].draw(screen)
            if grid_choices[i][0].check_click():
                choice = grid_choices[i][2]
                terminate = True

        pygame.display.flip()

    return choice


def algo_gui(font, width, height, top_pad, right_pad, algo):
    """Created the gui on which the """
    algo_dict = {1: "Breadth first search", 2: "Depth first search", 3: "A*", 4: "None"}

    title_font = pygame.font.SysFont("arial", 50)
    button_font = pygame.font.SysFont("sanscomic", 40)

    title_text = algo_dict[algo]
    horizontal_text = "Space: reset start-end    R : reset the grid size    S :  search algo"
    t_text = Text(title_font, (90, 0), width - 2 * right_pad, 70, title_text, (225, 105, 14), (80, 80, 80))
    h_text = Text(font, (90, 60), width - 2 * right_pad, 50, horizontal_text, (0, 0, 0), (80, 80, 80))

    button_h = 90
    start_button = Button(f"Start", 80, 60, (width + 10, 210 + 1 * button_h), button_font)

    collection = Text_Collection([h_text, t_text])

    return collection, start_button
