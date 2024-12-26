from PIL import Image
import numpy as np
import torch
from yolov5 import YOLOv5  # Assuming this is your YOLOv5 model import

def classify_image(image_file):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')
    # Read the uploaded image
    image = Image.open(image_file)  # Use Pillow to open the file
    image_array = np.array(image)  # Convert to a NumPy array

    # Ensure the image is in the right format for YOLOv5
    if len(image_array.shape) == 2:  # Grayscale to RGB
        image_array = np.stack((image_array,) * 3, axis=-1)
    elif image_array.shape[2] == 4:  # RGBA to RGB
        image_array = image_array[:, :, :3]

    # Use YOLO model to classify the image
    results = model(image_array)
    classes = results.pred[0]  # Adjust based on YOLO's output format
    return classes

