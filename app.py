from flask import Flask, request, render_template
from src.object_classifier import classify_image
from src.sparql_queries import fetch_concept_details
from flask import Flask, request, render_template
import os
# from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Define the key

# Ensure the folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = None
        detections = []

        # Handle file upload
        if 'file' in request.files and request.files['file']:
            image_file = request.files['file']
            image, detections = classify_image(image_file)

        # Handle URL input
        elif 'url' in request.form and request.form['url']:
            url = request.form['url']
            try:
                response = requests.get(url)
                image_file = BytesIO(response.content)
                image, detections = classify_image(image_file)
            except Exception as e:
                return f"Error processing URL: {e}"

        # Fetch concept details for each detected class
        concept_details = {}
        for detection in detections:
            class_name = detection['class']
            descriptions = fetch_concept_details(class_name)
            concept_details[class_name] = descriptions

        # Save the annotated image
        if image:
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "annotated_image.jpg")
            image.save(output_path)

        return render_template("results.html", detections=detections, image_path=output_path, concept_details=concept_details)

    return render_template("index.html")

app.run(debug=True)
