from flask import Flask, request, jsonify
# from mallook import analyze_file

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # for example, 16 megabytes
app.run(host='0.0.0.0', port=5000)

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
        # Process the file here (e.g., save it, analyze it, etc.)
        
        return jsonify({"hello": "world"})  # or your actual response after processing
    else:
        return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)