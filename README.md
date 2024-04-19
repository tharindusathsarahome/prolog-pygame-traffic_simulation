# Prolog-PyGame Traffic Simulation System

![Simulation Screenshot](https://github.com/tharindusathsarahome/prolog-pygame-traffic_simulation/blob/main/image.png)

## Overview

This project is a Prolog traffic simulation system implemented using Python Pygame. The simulation allows vehicles to travel along predefined paths within an intersection while considering traffic congestion. It utilizes Prolog to determine the shortest path for each vehicle based on current traffic conditions.

## Features

- **Vehicle Simulation**: Simulates various types of vehicles traveling within an intersection.
- **Dynamic Pathfinding**: Utilizes Prolog to dynamically calculate the shortest path for each vehicle based on traffic congestion.
- **Collision Detection**: Implements collision detection to prevent vehicles from colliding with each other.

## Requirements

- Python 3
- Pygame
- pyswip
- prolog

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/prolog-traffic-simulation.git
    ```

2. Navigate to the project directory:

    ```bash
    cd prolog-traffic-simulation
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the simulation:

    ```bash
    python main.py
    ```

## How it Works

The simulation consists of two main components:

- **Python Pygame Interface**: Handles the graphical interface and vehicle movement.
- **Prolog Backend**: Determines the shortest path for each vehicle based on traffic conditions.

The simulation utilizes Prolog's logic programming capabilities to calculate the optimal route for each vehicle dynamically. This information is then used by the Python Pygame interface to simulate vehicle movement within the intersection.

## Acknowledgments

- Special thanks to [Pygame](https://www.pygame.org/) and [pyswip](https://github.com/yuce/pyswip) for their contributions to this project.