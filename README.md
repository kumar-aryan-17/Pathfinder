# Pathfinding Visualizer

A simple and interactive **Pathfinding Algorithm Visualizer** built using **Python and Pygame**. This project allows you to visualize popular pathfinding algorithms like **DFS, BFS, Dijkstra's Algorithm, and A\*** in real-time on a customizable grid. It also includes features like a home screen, algorithm selection, and a reset option.

## Features

- Home Screen Interface with algorithm selection
- Supports the following algorithms:
  - Dijkstra's Algorithm
  - A* Search Algorithm
  - Depth First Search (DFS)
  - Breadth First Search (BFS)

- Visual differentiation of different searching algorithms
- Reset button ('R') to return to the home screen and return to menu with ('M') button
- Real-time grid updates
- Intuitive and simple user interface


## Demo Video
![Demo](demo_gif.gif)

### Watch the full video [here](https://www.youtube.com/watch?v=h-Y4taHBi_c).

## How it works

- Select the algorithm which you want to run
- Click on play
- When you once click on the board, it will create a start node. The second click will create the end node and rest other clicks will create barriers
- Left clicking any node will delete it and the next right click will allow you recreate the node deleted
- Press on SPACE BAR to run the search
- Press 'r' to reset the board
- Press 'm' to return to menu


## Installation

1. **Clone the repository:**

    git clone https://github.com/kumar-aryan-17/Pathfinder.git

2. **Navigate to the project directory:**

    cd Pathfinder

3. **Install Project dependencies:**

     pip3 install pygame_menu (Mac/Linux)
     pip install pygame_menu (Windows)

4. **Run the Project:**

     python3 main.py




   




