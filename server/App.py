from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS
from Solve import imageSolve, gridSolve, getTargetPath

app = Flask(__name__)
CORS(app)

@app.route('/api/gridSolver', methods=['POST'])
def grid(): 
    data = request.json
    result = gridSolve(data['grid'])
    return jsonify({ 'status' : 'success', 'valid' : result.valid, 'solution' : result.solution, 'message' : result.message })

@app.route('/api/imageSolver', methods=['POST'])
def image():
    if 'image' not in request.files:
        return jsonify({'status' : 'fail', 'error': 'No image part'})
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({'status' : 'fail', 'error': 'No selected file'})

    target = getTargetPath()
    filename = secure_filename(image.filename)
    image.save("/".join([target, filename]))
    result = imageSolve(filename)
    return jsonify({ 'status' : 'success', 'valid' : result.valid, 'solution' : result.solution, 'message' : result.message })

if __name__ == '__main__':
    app.run(debug=True)