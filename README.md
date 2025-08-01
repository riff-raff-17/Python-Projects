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

## 🧭 Pathfinding Visualization

This project is a visual representation of the A* pathfinding algorithm, showing how it efficiently finds the shortest path from a start point to a goal on a grid, while avoiding obstacles.

### Features

- Visualizes the step-by-step process of A* pathfinding
- Supports grid editing: add/remove obstacles
- Interactive start and end node placement
- Highlights open and closed sets in real-time
- Shows final path after successful search

A* is a popular graph traversal and pathfinding algorithm used in games, robotics, and navigation systems. It combines:

- g(n): the cost from the start node to the current node
- h(n): the heuristic estimate from the current node to the end
- f(n) = g(n) + h(n): total estimated cost of the cheapest solution through n

The default heuristic used is Manhattan distance. You can switch to Euclidean or Diagonal if needed.

This visualizer shows:

    🟧 Start node

    🟦 End node

    ⬛ Obstacles (walls)

    🟩 Open set (nodes to be evaluated)

    🟥 Closed set (nodes already evaluated)

    🟪 Final path (shortest route found)

### 🧹 'Roomba' pathfinding

Simulates a Roomba-style robot navigating a 2D room and avoiding obstacles using intelligent pathfinding. Similar to the previous, using Pygame to visualize the path the Roomba takes.

### Features

- Roomba-like robot that moves from start to finish
- Avoids obstacles (walls, furniture)
- Efficient path planning using A* algorithm
- Real-time visualization of robot movement 

The visualizer shows how to robot navigates from start to end and can be interrupted and updated at any time.

## Mediapipe
This directory contains various image recognition projects using MediaPipe. Current projects include:

**🎨 Color Recognition with UGOT**
- Recognizes RGB colors using OpenCV.
- Integrated with UGOT, a robot platform, to respond to detected colors.

**🎮 Catching Game with Pygame and MediaPipe Hands**
- A simple game built with Pygame.
- Uses MediaPipe Hands to detect hand movements for controlling the game.

**🦾Mechanical Arm Control**
- Adapted from the catching game.
- Uses hand movement data to control a mechanical arm.

 **👨Facial Recognition**
- rec_face.py has both simple facial recognition (face present or not) as well as the facial mesh for even more precise facial recognition 
- id_face.py allows recognition of specific faces uploaded into faces folder

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

## 🧮 PyTorch / Digit Classification

This project uses the MNIST dataset to train a neural network with PyTorch for handwritten digit recognition. It also includes an interactive Tkinter drawing app that allows you to test the model in real-time by drawing digits.

### Features:

**Model Training**
* Trains on the MNIST dataset of handwritten digits (0–9).
* Configurable network architecture and training parameters.
* Evaluates accuracy on test data.

**Digit Drawing App**
* Built with Tkinter for simple GUI interaction.
* Users can draw digits on a canvas.
* The trained model predicts the digit in real time.
* Supports clearing and redrawing for multiple tests.

## 🤖 Ollama / Voice-Controlled Robot

This project integrates Ollama for voice recognition and control of a robot. Spoken commands are converted into actions, allowing hands-free operation and real-time interaction.
### Features

**Voice Command Processing**
* Uses Ollama to capture and interpret spoken commands.
* Commands mapped to robot actions (e.g., move forward, turn left, stop).

**Robot Control** 
* Interfaces with a robot platform for motion execution.
* Can be extended for custom commands and behaviors.

**Interactive Feedback**
* The robot responds in real-time to recognized commands.
* Logs recognized commands and actions for debugging.

