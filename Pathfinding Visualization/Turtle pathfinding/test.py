import turtle
import random
import collections
import time

# configuration
CELL_SIZE = 20
GRID_W, GRID_H = 20, 15
WALL_PROB = 0.25
DELAY = 0.01  # seconds between steps

# set up screen
screen = turtle.Screen()
screen.setup(GRID_W * CELL_SIZE + 50, GRID_H * CELL_SIZE + 50)
screen.title("Maze BFS Pathfinding")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.penup()

# Draw a filled square at grid coord (x,y)
def draw_cell(x, y, color):
    pen.goto(x * CELL_SIZE - (GRID_W*CELL_SIZE)/2,
             (GRID_H*CELL_SIZE)/2 - y * CELL_SIZE)
    pen.fillcolor(color)
    pen.begin_fill()
    for _ in range(4):
        pen.pendown()
        pen.forward(CELL_SIZE)
        pen.right(90)
    pen.end_fill()
    pen.penup()

# generate random maze: True=wall, False=free
grid = [[random.random() < WALL_PROB for _ in range(GRID_W)]
        for _ in range(GRID_H)]

start = (0, 0)
goal = (GRID_W - 1, GRID_H - 1)
grid[start[1]][start[0]] = False
grid[goal[1]][goal[0]] = False

# draw initial maze
for y in range(GRID_H):
    for x in range(GRID_W):
        draw_cell(x, y, "black" if grid[y][x] else "white")

screen.exitonclick()