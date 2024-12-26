from flask import Flask, request, render_template
from src.object_classifier import classify_image
from src.sparql_queries import fetch_concept_details

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = request.files["file"]
        classes = classify_image(image)
        details = [fetch_concept_details(cls) for cls in classes]
        return render_template("results.html", details=details)
    return render_template("index.html")

app.run(debug=True)
