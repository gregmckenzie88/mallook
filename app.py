import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
# from mallook import analyze_file

# set app configs
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # for example, 16 megabytes
# app.run(host='0.0.0.0', port=5000)

# ensure exe route exists
exe_directory = "data/input/files"
if not os.path.exists(exe_directory):
    os.makedirs(exe_directory)

# ensure image route exists
image_directory = "data/output/files"
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

# declare route
@app.route('/classify', methods=['POST'])
def classify():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    # If the user does not select a file
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check the file type here (for an .exe file)
    if file and file.filename.endswith('.exe'):
        # save file to disk
        filename = secure_filename(file.filename)
        file.save(os.path.join(exe_directory, filename))

        # run mallook

        # retrieve image from disk

        # pre-process image

        # create data batch for test data

        # get prediction

        # bundle results

        # clear exe and image directories

        # return payload

        # Your processing logic here

        return jsonify({"message": "File uploaded successfully"})
        # Process the file here (e.g., save it, analyze it, etc.)
        
        return jsonify({"hello": "world"})  # or your actual response after processing
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)