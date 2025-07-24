import matplotlib.pyplot as plt
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# Grid matrix (1 = walkable, 0 = obstacle)
matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Setup grid and A* finder
grid = Grid(matrix=matrix)
start = grid.node(0, 0)
end = grid.node(9, 9)
finder = AStarFinder()
path, runs = finder.find_path(start, end, grid)

print("Path found:", path)
print("Number of operations:", runs)

# Visualization
# Create a numpy array from the matrix
vis_grid = np.array(matrix)

# Convert obstacles (0) to -1 for better contrast
vis_grid = np.where(vis_grid == 0, -1, 0)

# Mark path on grid
for x, y in path:
    vis_grid[y][x] = 2  # mark path (use 2)

# Mark start and end separately
sx, sy = start.x, start.y
ex, ey = end.x, end.y
vis_grid[sy][sx] = 3  # Start
vis_grid[ey][ex] = 4  # End

# Create color map
cmap = plt.cm.get_cmap("Set1", 5)
colors = {
     -1: "black", # obstacle
     0: "white", # empty
     2: "skyblue", # path
     3: "green", # start
     4: "red" # end
}
# Build the color grid
color_grid = np.empty(vis_grid.shape, dtype=object)
for y in range(vis_grid.shape[0]):
    for x in range(vis_grid.shape[1]):
        color_grid[y, x] = colors.get(vis_grid[y, x], "white")

# Plot the grid
fig, ax = plt.subplots()
for y in range(vis_grid.shape[0]):
    for x in range(vis_grid.shape[1]):
        rect = plt.Rectangle((x, y), 1, 1, facecolor=color_grid[y, x], edgecolor="gray")
        ax.add_patch(rect)

ax.set_xlim(0, vis_grid.shape[1])
ax.set_ylim(0, vis_grid.shape[0])
ax.set_xticks(np.arange(vis_grid.shape[1]+1))
ax.set_yticks(np.arange(vis_grid.shape[0]+1))
ax.invert_yaxis()
ax.set_aspect('equal')
plt.grid(True)
plt.title("A* Pathfinding Visualization")
plt.show()
