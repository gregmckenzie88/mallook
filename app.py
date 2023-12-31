import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
# from flask_cors import CORS
from mallook import analyze_file
from utils import process_images, create_data_batches, load_model, get_pred_label, bundle_results

# set app configs
app = Flask(__name__)
# CORS(app)
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

processed_image_directory = "processed_images"
if not os.path.exists(image_directory):
    os.makedirs(image_directory)

full_model = load_model('models/2023111122-15431700685793-full-image-set-mobilenetv2-Adam.h5')

analyze_file()
# declare route
# @app.route('/classify', methods=['POST'])
# def classify():
#     # Check if a file is part of the request
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files['file']

#     # If the user does not select a file
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     # Check the file type here (for an .exe file)
#     if file and file.filename.endswith('.exe'):
#         # save file to disk
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(exe_directory, filename))

#         # run mallook
#         # analyze_file()

#         # retrieve image from disk

#         # pre-process image
#         stubbed_image_path = 'data/output/files/nearest_600/'
#         process_images(
#             source_dirs=[stubbed_image_path],
#             destination_dir=processed_image_directory
#         )

#         # create data batch for test data
#         test_filenames = [processed_image_directory + '/' + fname for fname in os.listdir(processed_image_directory)]
#         test_data = create_data_batches(test_filenames, test_data=True)
#         # full_model = load_model('models/2023111122-15431700685793-full-image-set-mobilenetv2-Adam.h5')
#         test_predictions = full_model.predict(test_data, verbose=1)
#         test_pred_labels = [get_pred_label(test_predictions[i]) for i in range(len(test_predictions))]

#         results = bundle_results(test_filenames, test_predictions)
#         print(results)

#         # get prediction

#         # bundle results

#         # clear exe and image directories

#         # return payload

#         # Your processing logic here

#         return jsonify({"message": "File uploaded successfully"})
#         # Process the file here (e.g., save it, analyze it, etc.)
        
#         return jsonify({"hello": "world"})  # or your actual response after processing
#     else:
#         return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)