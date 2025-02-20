import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import os
import shutil
import cv2

# suppress tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

MEASUREMENT = 'nearest'
DPI = "600"
IMAGE_SIZE = 224
WORKSPACE_BASE_URL = '../data/raw/'
PROCESSED_IMAGE_DIRECTORY = '../data/processed/processed_images'
RANDOM_STATE = 42
BATCH_SIZE = 1

unique_labels = np.unique(['benign', 'malicious'])

source_dirs = [
  f'{WORKSPACE_BASE_URL}/portable_executables/benign/{MEASUREMENT}_{DPI}',
  f'{WORKSPACE_BASE_URL}/portable_executables/malicious/{MEASUREMENT}_{DPI}'
]
# create destination directory
destination_dir = PROCESSED_IMAGE_DIRECTORY

def process_images(
    measurement=MEASUREMENT,
    dpi=DPI,
    size=(IMAGE_SIZE, IMAGE_SIZE),
    trim_axis=True,
    destination_dir=destination_dir,
    source_dirs=source_dirs
):
  """
  gathers image files from both benign and malicious file directories,
  optionally remove axis imformation from the image
  resize the image to desired width & height
  distribute all files in processed images directory
  """

  # process each image
  for source_dir in source_dirs:
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)

        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            # Read the image
            image = cv2.imread(file_path)

            # optionally remove axis from image
            if trim_axis:
              # Convert to grayscale and threshold to isolate the spectrogram
              gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
              _, thresholded = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

              # Find contours and get the largest one which should be the spectrogram
              contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
              largest_contour = max(contours, key=cv2.contourArea)

              # Get bounding box of the largest contour
              x, y, w, h = cv2.boundingRect(largest_contour)

              # Crop the image to the bounding box
              image = image[y:y+h, x:x+w]

            # Resize the cropped image
            resized_image = cv2.resize(image, size)

            # Save the processed image to the destination directory
            cv2.imwrite(os.path.join(destination_dir, file_name), resized_image)
  print("Images have been successfully pre-processed!")


# create a helper function for preproceesing the a single image
def process_image(image_path, img_size=IMAGE_SIZE):
  """
  Takes an image path and returns an image as a Tensor
  """
  # Take an image file path as input
  # Use Tensorflow to read the file and save it to a variable
  image = tf.io.read_file(image_path)
  # Turn our image into Tensors
  image = tf.image.decode_jpeg(image, channels=3)
  # convert the colour channel from 0-255 to 0-1 values
  image = tf.image.convert_image_dtype(image, tf.float32)
  # Resize the image to be a shape of 224 X 224
  image = tf.image.resize(image, size=[img_size, img_size])
  # return the modified image
  return image

# create a helper function to create a tuple of tensors
def get_image_label(image_path, label):
  """
  Takes an image path name and associated label, and returns a tuple with image and associated label
  """
  image = process_image(image_path)
  return image, label


# create a funciton to turn data into batches
def create_data_batches(X, y=None, batch_size=BATCH_SIZE, valid_data=False, test_data=False):
  """
  Create batches of data out of image X and label y pairs.
  It shuffles the data if it's training data, but does not shuffle if it's validation or test data.
  It also accepts test data with no labels
  """

  # If the data is a test dataset, we don't have lables
  if test_data:
    print('Creating test data batches...')
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X))) # only filepaths -- no labels
    data_batch = data.map(process_image).batch(batch_size)
    return data_batch

  # if it's a valid dataset, we do not need to shuffle it
  elif valid_data:
    print('Creating valid data batches...')
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y))) # including both file paths and labels
    data_batch = data.map(get_image_label).batch(batch_size)
    return data_batch

  else:
    print('Creating training data batches...')
    # Turn file paths and labels into tensors
    data = tf.data.Dataset.from_tensor_slices((
        tf.constant(X),
        tf.constant(y)
    )) # including both file paths and labels
    # shuffle path names and labels prior to mapping is faster than mapping unpacked image tensors
    data = data.shuffle(buffer_size=len(X))

    data = data.map(get_image_label)
    data_batch = data.batch(batch_size)
    return data_batch
  

# and for loading a model into a notebook
def load_model(model_path):
    """
    loads a saved model from a specified path
    """
    print(f"loading saved model from {model_path}...")

    # load in our model!
    model = tf.keras.models.load_model(
      model_path,
      custom_objects={
          'KerasLayer': hub.KerasLayer # denote our layer imported from tensorhub
      }
    )

    return model

def get_pred_label(prediction_probabilities):
  """
  turns an array of prediction probabilities into a label
  """
  return unique_labels[np.argmax(prediction_probabilities)]

def bundle_results(filenames, predictions):
    pred_labels = [get_pred_label(predictions[i]) for i in range(len(predictions))]
    result = []

    for file, prediction, label in zip(filenames, predictions, pred_labels):
        filename_without_path = os.path.basename(file)
        stripped_filename = filename_without_path.replace('_nearest_600_.png', '')
        result.append({
            "file_name": f"{stripped_filename}.exe",
            "confidence": str(round(max(prediction), 2)),
            "classification": label
        })

    return result

def clear_directory(dir_path):
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        print(f"Directory {dir_path} does not exist.")
