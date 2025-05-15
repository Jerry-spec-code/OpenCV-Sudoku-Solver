# OpenCV-Sudoku-Solver

# Project Demo:
https://youtu.be/vm5mjRRbf_k

# What is it?
A Flask/React application that takes an image of an unsolved sudoku puzzle as input and outputs a valid solution.

## Languages/Frameworks used: 
1. Python
2. TypeScript
3. HTML/CSS
4. Flask
5. React
6. Material-UI
7. Makefile

## Key features: 
1. The user uploads an image of an unsolved sudoku puzzle and clicks 'solve' when uploaded. 
2. The program outputs 'invalid puzzle' if the image is not a readable sudoku puzzle. 
3. The program uses OpenCV and a custom OCR machine learning model to read the image. 
4. Afterwards, the program solves the puzzle using 3 optimized logical deduction/backtracking algorithms.
5. The solution is then displayed on the frontend via React, also identifying puzzles with multiple solutions. 
6. The user also has the option of manually filling a Sudoku Grid by clicking on 'Fill in the grid instead'.

## Screenshots of Project
<img width="1431" alt="image" src="https://github.com/Jerry-spec-code/OpenCV-Sudoku-Solver/assets/78711575/b61326c5-51d4-4275-b1a2-fa4f73b3b7f9">

##  Frontend Environment variables 

| Variable    | Description                                 |
| ----------- | ------------------------------------------- |
| NODE_ENV    | `development`                               |

Note: Frontend Environment variables can be supplied via a `.env` file in the client directory. See  `./client/example.env` for an example 


## Project Setup

To run the project, you will need to open two separate terminals.
- In the first terminal, run `make backend`. This will install all the Python packages in a virtual environment and run the server on port 5000.
- In the second terminal, run `make frontend`. This will install all the TypeScript packages and run the application on port 3000. Open http://localhost:3000 to view the result in your browser.

### Other Make Commands
| Command                  | Description                                                   |
| -----------------------  | ------------------------------------------------------------- |
| `make install_frontend`  | Install all the frontend TypeScript packages                  |
| `make start_frontend`    | Start the frontend without installing packages                |
| `make install_backend`   | Setup virtual environment and install backend Python packages |
| `make start_backend`     | Start the server without installing packages                  |
| `make clean_backend`     | Destroys the virtual environment and removes Python packages  |
