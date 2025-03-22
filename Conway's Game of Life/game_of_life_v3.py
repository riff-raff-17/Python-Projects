# Adds some of the famous game of life patterns, but without custom drawing

import pygame
import numpy as np

# Screen size
WIDTH, HEIGHT = 1000, 800
CELL_SIZE = 20
FPS = 20
SIDEBAR_WIDTH = 150

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_COLOR = (40, 40, 40)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HIGHLIGHT = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)

# Grid
ROWS = HEIGHT // CELL_SIZE
COLS = (WIDTH - SIDEBAR_WIDTH) // CELL_SIZE

# Initialize grid to all zeros
grid = np.zeros((ROWS, COLS), dtype=int)

# Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Base patterns
PATTERNS = {
    'glider': [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1]
    ],
    'small_exploder': [
        [0, 1, 0],
        [1, 1, 1],
        [1, 0, 1],
        [0, 1, 0]
    ],
    'pulsar': [
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0]
    ],
    'glider_gun': [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    'block': [
    [1, 1],
    [1, 1]
    ],
    'blinker': [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ],
    'toad': [
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ],
    'beacon': [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ]
}

# Button positions
buttons = [
    ('Glider', (WIDTH - SIDEBAR_WIDTH + 10, 50)),
    ('Small Exploder', (WIDTH - SIDEBAR_WIDTH + 10, 100)),
    ('Pulsar', (WIDTH - SIDEBAR_WIDTH + 10, 150)),
    ('Glider Gun', (WIDTH - SIDEBAR_WIDTH + 10, 200)),
    ('Block', (WIDTH - SIDEBAR_WIDTH + 10, 250)),
    ('Blinker', (WIDTH - SIDEBAR_WIDTH + 10, 300)),
    ('Toad', (WIDTH - SIDEBAR_WIDTH + 10, 350)),
    ('Beacon', (WIDTH - SIDEBAR_WIDTH + 10, 400)),
    ('Clear', (WIDTH - SIDEBAR_WIDTH + 10, 450))
]

selected_pattern = None

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if grid[row][col] == 1 else BLACK
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1) # grid lines

def update_grid():
    global grid
    new_grid = grid.copy()
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = np.sum(grid[row-1:row+2, col-1:col+2]) - grid[row][col]
            if grid[row][col] == 1: # Cell is alive
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0 # Underpopulation or Overpopulation
            else: # Cell is dead
                if neighbors == 3:
                    new_grid[row][col] = 1 # Reproduction
    grid = new_grid

def place_pattern(pattern_name, x, y):
    pattern = PATTERNS.get(pattern_name)
    if pattern:
        for row in range(len(pattern)):
            for col in range(len(pattern[0])):
                if 0 <= row + y < ROWS and 0 <= col + x < COLS:
                    grid[row + y][col + x] = pattern[row][col]

def handle_mouse():
    global selected_pattern
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        x, y = pygame.mouse.get_pos()
        if x < WIDTH - SIDEBAR_WIDTH:
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            if selected_pattern:
                place_pattern(selected_pattern, col, row)
            else:
                x, y = pygame.mouse.get_pos()
                row = y // CELL_SIZE
                col = x // CELL_SIZE
                grid[row][col] = 1 if grid[row][col] == 0 else 0

def draw_buttons():
    for text, (x, y) in buttons:
        color = BUTTON_HIGHLIGHT if selected_pattern == text.lower().replace(' ', '_') else BUTTON_COLOR
        rect = pygame.Rect(x, y, SIDEBAR_WIDTH - 20, 30)
        pygame.draw.rect(screen, color, rect)
        label = font.render(text, True, TEXT_COLOR)
        screen.blit(label, (x + 10, y + 5))

def handle_buttons(x, y):
    global selected_pattern
    for text, (bx, by) in buttons:
        rect = pygame.Rect(bx, by, SIDEBAR_WIDTH - 20, 30)
        if rect.collidepoint(x, y):
            if text == 'Clear':
                grid.fill(0)
            else:
                selected_pattern = text.lower().replace(' ', '_')

def main():
    running = True
    paused = True

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_buttons(*event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused

        handle_mouse()

        if not paused:
            update_grid()

        pygame.display.flip()
        clock.tick(FPS) # FPS

    pygame.quit()

if __name__ == "__main__":
    main()
