# OpenCV-Sudoku-Solver

# What is it?
A Flask/React application that takes an image of an unsolved sudoku puzzle as input and outputs a valid solution.

## Languages/Frameworks used: 
1. Python
2. TypeScript
3. HTML/CSS
4. Java
5. Flask
6. React
7. Material-UI

## Key features: 
1. The user uploads an image of an unsolved sudoku puzzle and clicks 'solve' when uploaded. 
2. The program outputs 'invalid puzzle' if the image is not a readable sudoku puzzle. 
3. The program uses OpenCV and a custom OCR machine learning model to read the image and output the corresponding puzzle to a text file. 
4. Afterwards, the program uses Jpype to connect the python code to a custom backend Java API that solve the puzzle using 3 optimized solving algorithms.
5. The solution is then outputted to a text file which is then read via python and displayed via HTML/CSS, also identifying puzzles with multiple solutions. 
6. The user also has the option of manually filling a Sudoku Grid by clicking on 'Fill in the grid instead'.

## Screenshots of Project
<img width="1429" alt="image" src="https://github.com/Jerry-spec-code/OpenCV-Sudoku-Solver/assets/78711575/8f6897c5-9dd5-4e27-b10a-cec3d69f1565">


### Installing required pip packages: Run the commands below 

```sh
cd ./server
python3 -m venv venv (Set up the virtual environment)
. venv/bin/activate  (Activate the virtual environment)
pip3 install -r requirements.txt (install the required packages)
```

### Backend Flask Setup

```sh
cd ./server
javac App.java (Compiles the java code)
python3 App.py 
```

### Frontend React Setup

```sh
cd ./client
npm install
npm start
```

This will run the application on port 3000. Open http://localhost:3000 to view it in your browser.

##  Frontend Environment variables 

| Variable    | Description                                 |
| ----------- | ------------------------------------------- |
| NODE_ENV    | `development`                               |

Note: Frontend Environment variables can be supplied via a `.env` file in the client directory. See  `./client/example.env` for an example 

