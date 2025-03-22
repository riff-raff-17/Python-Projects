# Creates menus for the patterns, as well as bringing back drawing functionality

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
    ],
    'lwss': [
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0]
    ],
    'mwss': [
        [0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0]
    ],
    'hwss': [
        [0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0, 0],
    ]
}

# Button positions
buttons = [
    # Stationary Patterns
    ('Stationary', (WIDTH - SIDEBAR_WIDTH + 10, 30)),  # Category header
    ('Block', (WIDTH - SIDEBAR_WIDTH + 10, 60)), 

    # Beacons (Oscillators)
    ('Beacons', (WIDTH - SIDEBAR_WIDTH + 10, 110)),  # Category header
    ('Blinker', (WIDTH - SIDEBAR_WIDTH + 10, 140)),
    ('Small Exploder', (WIDTH - SIDEBAR_WIDTH + 10, 170)),
    ('Pulsar', (WIDTH - SIDEBAR_WIDTH + 10, 200)),
    ('Toad', (WIDTH - SIDEBAR_WIDTH + 10, 230)),
    ('Beacon', (WIDTH - SIDEBAR_WIDTH + 10, 260)),

    # Gliders
    ('Gliders', (WIDTH - SIDEBAR_WIDTH + 10, 310)),  # Category header
    ('Glider', (WIDTH - SIDEBAR_WIDTH + 10, 340)),
    ('LWSS', (WIDTH - SIDEBAR_WIDTH + 10, 370)),
    ('MWSS', (WIDTH - SIDEBAR_WIDTH + 10, 400)),
    ('HWSS', (WIDTH - SIDEBAR_WIDTH + 10, 430)),
    ('Glider Gun', (WIDTH - SIDEBAR_WIDTH + 10, 460)),

    # Other Actions
    ('Brush', (WIDTH - SIDEBAR_WIDTH + 10, 510)),
    ('Clear', (WIDTH - SIDEBAR_WIDTH + 10, 540))
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
        if text in ["Stationary", "Beacons", "Gliders"]:  # Category Headers
            label = font.render(text, True, TEXT_COLOR)
            screen.blit(label, (x + 10, y + 5))  # Display only text
        else:  # Actual buttons
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
            elif text == 'Brush':
                selected_pattern = None
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

        status_text = "Paused" if paused else "Running"
        status_color = (200, 50, 50) if paused else (50, 200, 50) 
        status_label = font.render(status_text, True, status_color)
        screen.blit(status_label, ((WIDTH - SIDEBAR_WIDTH) // 2 - 30, 10))

        pygame.display.flip()
        clock.tick(FPS) # FPS

    pygame.quit()

if __name__ == "__main__":
    main()
