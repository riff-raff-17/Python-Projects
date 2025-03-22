# Python Projects

TODO: Write up description for each project

## NEAT Projects

### NEAT Dino
Chrome dinosaur game using NEAT. Showcase of basic NEAT implementation.

### NEAT Car
Implementation of self driving car using NEAT. Also includes side programs aimed at increasing the user driving functionality. Part2a.py contains a simple program with an overall timer, a time since last death, and collision on the grass. Part2b.py contains a more complex program including road checkpoints, a splits timer, and a leaderboard which saves the best times.

## OpenCV
Using OpenCV to do various image recognition projects. Current projects include:

* Color recognition with UGOT. RGB only
* Simple catching game built with Pygame and MediaPipe Hands.
* Simple mechanical arm control adapted from catching game

## Conway's Game of Life

This is a Python implementation of Conway's Game of Life using pygame. The Game of Life is a cellular automaton devised by mathematician John Conway. It consists of a grid of cells that can be either alive or dead. The game evolves through a series of generations based on a set of simple rules.

**Start/Stop the Simulation**
* Press spacebar to begin the simulation.
* Press spacebar to pause the simulation.

**Drawing and Erasing**
* Use the "Brush" button to switch to drawing mode. Left-click on the grid to add live cells.
* Use the "Eraser" button to switch to erasing mode. Left-click on the grid to remove live cells.

**Pattern Selection**
* Open the pattern dropdown to select predefined patterns (like gliders or oscillators).
* Left-click on the grid to place the selected pattern.

**Clear the Grid**
* Click the "Clear" button to reset the grid.

Game Rules
1. Any live cell with fewer than two live neighbors dies (underpopulation).
2. Any live cell with two or three live neighbors survives.
3. Any live cell with more than three live neighbors dies (overpopulation).
4. Any dead cell with exactly three live neighbors becomes alive (reproduction).
