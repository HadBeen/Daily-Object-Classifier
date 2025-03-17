import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
from ultralytics import YOLO

def classify_image(image_file):
    # Load the YOLOv5 model
    model = YOLO("yolov5s.pt")

    # Read the uploaded image
    image = Image.open(image_file).convert("RGB")
    image_array = np.array(image)

    # Run the YOLO model
    results = model(image_array)

    # Prepare drawing
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except IOError:
        font = ImageFont.load_default()

    detections = []

    # Iterate over detections
    for result in results:
        for idx, box in enumerate(result.boxes):
            class_id = int(box.cls.item())  # Extract class index
            confidence = float(box.conf.item())  # Confidence score
            xmin, ymin, xmax, ymax = map(int, box.xyxy[0].tolist())  # Bounding box

            label = f"{idx + 1}: {model.names[class_id]} ({confidence:.2f})"

            random_color = tuple(random.randint(0, 255) for _ in range(3))
            draw.rectangle([xmin, ymin, xmax, ymax], outline=random_color, width=3)
            draw.text((xmin, ymin), label, fill=random_color, font=font)

            detections.append({
                "id": idx + 1,
                "class": model.names[class_id],
                "confidence": confidence,
                "bbox": [xmin, ymin, xmax, ymax]
            })

    return image, detections
