from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, escape
from flask_cors import CORS
from Solve import solve, gridSolve, setTargetPath

app = Flask(__name__)
CORS(app)

@app.route('/api/gridSolver', methods=['POST'])
def grid(): 
    data = request.json
    inputList = data['grid']
    result = gridSolve(inputList)
    return { 'status' : 'success', 'result' : result}

@app.route('/api/imageSolver', methods=['POST'])
def image():
    pass

if __name__ == '__main__':
    app.run(debug=True)