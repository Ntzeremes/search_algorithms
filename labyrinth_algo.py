""""Has the classes that are used to create the labyrinth inside the grid
The function path inside the labyrinth class is the one that starts end generates the labyrinth
inside the grid"""

import time
import random
import pygame


class Node:
    """A node is a part of the path. Each node is connected with the previous one, called parent.
    All the nodes connected create the path. Many paths ,like branched of a tree create the labyrinth"""

    propagate_chance = 0.5
    same_direction = 0.65

    def __init__(self, parent, pos):
        self.parent = parent
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def can_insert(self, width, height, grid):
        """Checking if the Node can enter the grid. In order for it to enter it must have only 1 neighbor, it's parent.
        If it had more than, we wouldn't have a tree like structure labyrinth, because the branches would intermingle."""
        n = 0
        for i in range(2):
            for j in range(2):
                x = self.pos_x + i * (-1) ** j
                y = self.pos_y + (1 - i) * (-1) ** j
                if 0 <= x < width and 0 <= y < height:
                    if grid[y][x] is not None:
                        n += 1
        return True if n == 1 else False

    def neighbors(self, labyrinth):
        """checking the grid positions on the top, bottom, left and right of the Node.
        The parent node is excluded."""

        neighbors = []

        # Adding neighbors that are on top, bottom , right and left in the labyrinth that we haven't visited so far.
        # Checking if each neighbor has other neighbors apart from the parent node.
        # We don't want them to have other nodes around cause the paths will intermingle otherwise.

        # top
        if self.pos_y - 1 >= 0:
            if labyrinth.grid[self.pos_y - 1][self.pos_x] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + i * (-1) ** j
                        y = self.pos_y - 1 + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.width and 0 <= y < labyrinth.height:
                            if labyrinth.grid[y][x] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x, self.pos_y - 1))

        # bottom
        if self.pos_y + 1 < labyrinth.height:
            if labyrinth.grid[self.pos_y + 1][self.pos_x] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + i * (-1) ** j
                        y = self.pos_y + 1 + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.width and 0 <= y < labyrinth.height:
                            if labyrinth.grid[y][x] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x, self.pos_y + 1))

        # left
        if self.pos_x - 1 >= 0:
            if labyrinth.grid[self.pos_y][self.pos_x - 1] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x - 1 + i * (-1) ** j
                        y = self.pos_y + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.width and 0 <= y < labyrinth.height:
                            if labyrinth.grid[y][x] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x - 1, self.pos_y))

        # right
        if self.pos_x + 1 < labyrinth.width:
            if labyrinth.grid[self.pos_y][self.pos_x + 1] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + 1 + i * (-1) ** j
                        y = self.pos_y + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.width and 0 <= y < labyrinth.height:
                            if labyrinth.grid[y][x] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x + 1, self.pos_y))
        return neighbors

    def children(self, lab):
        """choosing the child node of the current node.
        If the parent node has a parent itself, then there is a higher chance that the child will follow the direction
        of the parent. This is done to create somewhat straight paths.
        There is also a small chance that the node will have a second child, that will create a new branch-path."""

        neighbors = self.neighbors(lab)

        if not neighbors:
            return None
        second_child = None

        # Giving the same direction coming from parent a higher chance
        if self.parent:

            i = random.random()
            # keep parent's direction,it has a higher chance
            parents_direction_node = (2 * self.pos_x - self.parent[0], 2 * self.pos_y - self.parent[1])
            if parents_direction_node in neighbors:
                # keep direction randomly or if only one neighbor
                if len(neighbors) == 1 or i < Node.same_direction:
                    first_child = Node((self.pos_x, self.pos_y), parents_direction_node)
                # else choose randomly between the other neighbors excluding the parent_direction node
                else:
                    neighbors.remove(parents_direction_node)
                    first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))
            # if there is no node in parent direction chose randomly
            else:
                first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))
        else:
            # if no parent we are at the starting Node, in case of starting the labyrinth,
            # choose randomly from the neighbors
            first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))

        l = len(neighbors)

        # Chance to create a new branch
        if l == 0:
            # No neighboors left so we exit
            return None
        elif l > 1:
            propagate = random.random()
            if propagate < Node.propagate_chance:
                neighbors.remove((first_child.pos_x, first_child.pos_y))
                second_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))

        if second_child:
            return [first_child, second_child]

        return [first_child]

    @staticmethod
    def change_propagate(sign):
        if sign == "+":
            Node.propagate_chance += 0.02
            if Node.propagate_chance > 1:
                Node.propagate_chance = 0
        else:
            Node.propagate_chance -= 0.02
            if Node.propagate_chance < 0:
                Node.propagate_chance = 1

        Node.propagate_chance = round(Node.propagate_chance, 2)

        return Node.propagate_chance

    @staticmethod
    def change_direction(sign):
        if sign == "+":
            Node.same_direction += 0.02
            if Node.same_direction > 1:
                Node.same_direction = 0
        else:
            Node.same_direction -= 0.02
            if Node.same_direction < 0:
                Node.same_direction = 1

        Node.same_direction = round(Node.same_direction, 2)
        return Node.same_direction


class Labyrinth:
    """The class that creates the n x n grid of the labyrinth. Initially it is filled with None values, the path
    is represented by values 0. Also has some basic functions for extra utility - manipulation and the function that
    creates the path."""

    def __init__(self, width, height, screen_width, screen_height, screen, block, top_pad):
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.screen = screen
        self.block = block
        self.top_pad = top_pad
        self.empty = True

    # noinspection PyTypeChecker
    def insert(self, node):
        """inserts a node in grid and draws it"""
        x = node.pos_x
        y = node.pos_y
        self.grid[y][x] = 0
        if self.screen:
            pygame.draw.rect(self.screen, (175, 175, 175),
                             (x * self.block + 2, y * self.block + 2 + self.top_pad, self.block - 2, self.block - 2))
            pygame.display.flip()

    def draw_tiles(self):
        """When we choose a search algorithm , we draw the previously picked labyrinth"""
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y][x] is not None:
                    pygame.draw.rect(self.screen, (175, 175, 175),
                                     ( x * self.block + 2, y * self.block + 2 + self.top_pad,
                                       self.block - 2, self.block - 2))

    def reset(self):
        """resets the grid of labyrinth"""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

    def print_grid(self):
        for i in range(self.height):
            print(self.grid[i])
            print()

    def path(self, x, y, step=0):
        """This function generates a random path inside the grid.
        The path starts at a x,y point in the grid """

        self.empty = False

        start = Node(None, (x, y))
        current_nodes = []
        self.insert(start)
        first_children = start.children(self)
        if first_children:
            current_nodes.extend(first_children)

        while current_nodes:
            time.sleep(step)
            current_node = current_nodes.pop(0)
            if current_node.can_insert(self.width, self.height, self.grid):
                self.insert(current_node)

                children = current_node.children(self)
                if children:
                    current_nodes.extend(children)

    def draw_grid(self):
        """ Creates the height x width  grid of the labyrinth.
        Used when we start the program and every time we reset the labyrinth"""

        pygame.draw.rect(self.screen, (80, 80, 80), (0, self.top_pad, self.screen_width, self.screen_height))
        pygame.draw.line(self.screen, (0, 0, 0), (0, self.top_pad), (self.screen_width, self.top_pad), 2)
        for i in range(self.height - 1):
            pygame.draw.line(self.screen, (0, 0, 0), (0, (i + 1) * self.block + self.top_pad),
                             (self.screen_width, (i + 1) * self.block + self.top_pad),
                             2)
        for j in range(self.width):
            pygame.draw.line(self.screen, (0, 0, 0), ((j + 1) * self.block, self.top_pad),
                             ((j + 1) * self.block, self.screen_height + self.top_pad), 2)