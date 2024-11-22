from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS
from Solve import image_solve, grid_solve, get_target_path
from Response import Error

app = Flask(__name__)
CORS(app)

@app.route('/api/gridSolver', methods=['POST'])
def grid(): 
    data = request.json
    result = grid_solve(data['grid'])
    return jsonify(result.to_dict())

@app.route('/api/imageSolver', methods=['POST'])
def image():
    if 'image' not in request.files:
        return jsonify(Error(error='No image part').to_dict())
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify(Error(error='No selected file').to_dict())

    target = get_target_path()
    filename = secure_filename(image.filename)
    image.save("/".join([target, filename]))
    result = image_solve(filename)
    return jsonify(result.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
