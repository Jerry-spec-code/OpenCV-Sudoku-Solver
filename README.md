# OpenCV-Sudoku-Solver

# What is it?
The computer vision sudoku solver is a web application that takes an image of an unsolved sudoku puzzle as input and outputs a valid solution using Flask to deploy the application on Google App Engine. 

## Languages used: 
1. Python
2. Java
3. HTML/CSS

## Key features: 
1. The user uploads an image of an unsolved sudoku puzzle and clicks 'solve' when uploaded. 
2. The program outputs 'invalid puzzle' if the image is not a readable sudoku puzzle. 
3. The program uses OpenCV and a custom OCR machine learning model to read the image and output the corresponding puzzle to a text file. 
4. Afterwards, the program uses Jpype to connect the python code to a custom backend Java API that solve the puzzle using 3 optimized solving algorithms.
5. The solution is then outputted to a text file which is then read via python and displayed via HTML/CSS, also identifying puzzles with multiple solutions. 
6. The user also has the option of manually filling a Sudoku Grid by clicking on 'Fill in the grid instead'.

## Screenshots of Project
<img width="1440" alt="image" src="https://user-images.githubusercontent.com/78711575/171978390-3a4bd32d-c60f-4b77-ac74-9fb6af7caa90.png">
<img width="1434" alt="image" src="https://user-images.githubusercontent.com/78711575/170419328-596ba3f7-8ade-41ac-87f2-ad415b42a27a.png">
<img width="1427" alt="image" src="https://user-images.githubusercontent.com/78711575/170393835-1e5b7e20-1570-4e38-99b8-1ce9001c3a3e.png">
<img width="1429" alt="image" src="https://user-images.githubusercontent.com/78711575/170393844-cd466712-35b3-4d4a-bcf9-89e4bb08e391.png">

## Tools/Frameworks: 
1. Flask
2. OpenCV
3. Jpype 

### Installing required pip packages: Run the commands below 

```sh
cd ./src
python3 -m venv venv (Set up the virtual environment)
. venv/bin/activate  (Activate the virtual environment)
pip3 install -r requirements.txt (install the required packages)
```

### How to run this project?  

```sh
cd ./src
javac App.java (Compiles the java code)
python3 App.py 
```

Open http://127.0.0.1:5000/ to view the app in your browser.
