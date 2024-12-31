import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random


def classify_image(image_file):
    print("ff helllllloooo d")
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)    
    # Read the uploaded image
    image = Image.open(image_file).convert("RGB")
    image_array = np.array(image)
    
    # Run the YOLO model
    results = model(image_array)
    
    # Draw detections on the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=20)  # Replace with a path to a TTF font
    
    detections = []
    for idx, result in enumerate(results.xyxy[0]):  # Enumerate detections for numbering
        class_id, confidence, xmin, ymin, xmax, ymax = result[5], result[4], result[0], result[1], result[2], result[3]
        label = f"{idx + 1}: {results.names[int(class_id)]}"
        
        random_color = tuple(random.randint(0, 255) for _ in range(3))
        draw.rectangle([xmin, ymin, xmax, ymax], outline=random_color, width=3)
        draw.text((xmin, ymin), label, fill=random_color, font=font)
        
        detections.append({
            "id": idx + 1,
            "class": results.names[int(class_id)],
            "confidence": float(confidence),
            "bbox": [int(xmin), int(ymin), int(xmax), int(ymax)]
        })
    
    return image, detections

