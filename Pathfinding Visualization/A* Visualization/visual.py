'''Basic setup of Node class'''

import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding")

'''End of part 1'''

RED = (255, 0, 0)          # Closed set
GREEN = (0, 255, 0)        # Open set
WHITE = (255, 255, 255)    # Default/empty node
BLACK = (0, 0, 0)          # Barrier
PURPLE = (128, 0, 128)     # Final path
ORANGE = (255, 165, 0)     # Start node
GREY = (128, 128, 128)     # Grid lines
TURQUOISE = (64, 224, 208) # End node

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass # Big, will do later

    def __lt__(self, other):
        # less than: What happens if we compare two spots together
        return False
    
