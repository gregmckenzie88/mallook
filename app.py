import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from mallook import analyze_file
from utils import process_images, create_data_batches, load_model, get_pred_label, bundle_results, clear_directory

# set app configs
app = Flask(__name__)

# set max-size of file upload to 40 megs
app.config['MAX_CONTENT_LENGTH'] = 40 * 1024 * 1024  # for example, 40 megabytes

# set CORS Origins
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# ensure exe route exists
exe_directory = "data/input/files"
if not os.path.exists(exe_directory):
    os.makedirs(exe_directory)

# ensure image route exists
image_directory = "data/output/files"
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

processed_image_directory = "processed_images"
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

# load in TF model
full_model = load_model('models/2023111122-15431700685793-full-image-set-mobilenetv2-Adam.h5')

# declare classify route
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
        analyze_file()

        # pre-process image
        stubbed_image_path = 'data/output/files/nearest_600/'
        process_images(
            source_dirs=[stubbed_image_path],
            destination_dir=f"./{processed_image_directory}"
        )

        # generate prediction
        test_filenames = ["./" + processed_image_directory + '/' + fname for fname in os.listdir(processed_image_directory)]
        test_data = create_data_batches(test_filenames, test_data=True)
        test_predictions = full_model.predict(test_data, verbose=1)
        results = bundle_results(test_filenames, test_predictions)

        # clear exe and image directories
        directories = [exe_directory, image_directory, processed_image_directory]
        for directory in directories:
            clear_directory(directory)
        
        return jsonify(results[0])
    else:
        return jsonify({"error": "Invalid file type"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)