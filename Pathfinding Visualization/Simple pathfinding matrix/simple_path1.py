'''Basic pathfinding with A*'''
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# Create a grid represented as a matrix (1 for walkable, 0 for obstacle)
matrix = [
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 1]
]

# Initialize the grid and define start/end points
grid = Grid(matrix=matrix)
start = grid.node(0, 0)
end = grid.node(3, 3)

# Instantiate the A* finder
finder = AStarFinder()

# Find the path along with some statistics
path, runs = finder.find_path(start, end, grid)
print("Path found:", path)
print("Number of operations:", runs)
