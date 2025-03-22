# Python Projects

## NEAT Projects

### 🦖 NEAT Dino
This program is a NEAT-based AI implementation of the Chrome Dinosaur Game using pygame. The goal is to train neural networks to control dinosaurs, teaching them to avoid obstacles and maximize their score. The program includes the following features:

- **AI Learning:** Uses NEAT to train dinosaurs to avoid obstacles.
- **Obstacle Types:** Small and large cacti appear at random intervals.
- **Adaptive Difficulty:** Score limit increases with each generation.
- **Fitness-based Learning:** Fitness increases with survival time and decreases upon hitting obstacles.
- **Dynamic Population:** User can set the population size before starting the simulation.
- **Real-time Statistics:** Displays generation, game speed, score limit, and number of remaining dinosaurs.

**Game Loop**
1. The AI controls multiple dinosaurs using neural networks.
2. Each dinosaur decides whether to jump or keep running based on obstacle distance and position.
3. Fitness is calculated based on survival time and penalty for collisions.
4. NEAT adjusts the neural networks to improve performance over generations.


### 🚗 NEAT Car
This is a NEAT-based self-driving car simulation using Python's pygame and neat libraries. The program simulates a car navigating a track, controlled by a neural network trained using the NEAT algorithm. The goal is to train the car to avoid collisions and navigate efficiently using radar-based sensors.

Side project: Part2a.py contains a simple program with an overall timer, a time since last death, and collision on the grass. Part2b.py contains a more complex program including road checkpoints, a splits timer, and a leaderboard which saves the best times.

#### Main Components
Car Class:
- Controls the car's movement, rotation, and collision detection.
- Uses five radar sensors to measure distances from track boundaries.
- Inputs sensor data into the neural network to adjust driving decisions.
  
NEAT Integration:
- The neural network is evolved using the NEAT algorithm to maximize fitness.
- Fitness is increased based on how long the car survives and how far it drives.
  
Statistics:
- Displays the number of active cars and the current generation.
- Updates window title with the remaining time.

**Game Loop**
1. The neural network receives sensor data and outputs steering decisions.
2. The car drives and adjusts its direction based on network output.
3. If the car collides with a track boundary, it is removed.
4. The simulation ends when all cars crash or time runs out.

## OpenCV
This directory contains various image recognition projects using OpenCV. Current projects include:

**🎨 Color Recognition with UGOT**
- Recognizes RGB colors using OpenCV.
- Integrated with UGOT, a robot platform, to respond to detected colors.

**🎮 Catching Game with Pygame and MediaPipe Hands**
- A simple game built with Pygame.
- Uses MediaPipe Hands to detect hand movements for controlling the game.

**🦾Mechanical Arm Control**
- Adapted from the catching game.
- Uses hand movement data to control a mechanical arm.

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

## L4 Trial

