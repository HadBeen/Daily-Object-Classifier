from flask import Flask, request, render_template , send_from_directory
from src.object_classifier import classify_image
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL
import os
import requests
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Define the key
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


UPLOAD_FOLDER_RDF = 'static/rdf_files'
os.makedirs(UPLOAD_FOLDER_RDF, exist_ok=True)
app.config['UPLOAD_FOLDER_RDF'] = UPLOAD_FOLDER_RDF



def fetch_concept_details(concept):
    base_url = "http://api.conceptnet.io/c/en/"
    concept = concept.replace(" ", "_").lower()  # Format the concept properly

    response = requests.get(f"{base_url}{concept}")

    if response.status_code == 200:
        data = response.json()

        g = Graph()

        ns = {
            "ex": "http://example.org/"
        }

        if 'edges' in data:
            for edge in data['edges']:
                if 'end' in edge and 'label' in edge['end']:
                    concept_label = edge['end']['label']

                    concept_uri = URIRef(f"http://example.org/{concept}")
                    description_uri = URIRef(f"http://example.org/{concept_label.replace(' ', '_')}")

                    g.add((concept_uri, RDF.type, OWL.Class))
                    g.add((concept_uri, RDFS.label, Literal(concept)))
                    g.add((description_uri, RDFS.label, Literal(concept_label)))
                    g.add((concept_uri, RDFS.seeAlso, description_uri))

        # Save RDF file to the server's directory
        rdf_filename = f"{concept}_description.ttl"
        rdf_file_path = os.path.join(app.config['UPLOAD_FOLDER_RDF'], rdf_filename)
        g.serialize(destination=rdf_file_path, format="turtle")
        
        return rdf_file_path, rdf_filename
    else:
        return None, "Error fetching data"


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
        rdf_content = ""
        rdf_filename = ""
        
        # For the first detection (or all detections if necessary)
        if detections:
            for detection in detections:
                class_name = detection['class']
                descriptions = fetch_concept_details(class_name)
                concept_details[class_name] = descriptions
                
                # Generate RDF content for preview
                if descriptions:
                    rdf_content += f"### {class_name} ###\n"
                    for desc in descriptions:
                        rdf_content += f"{desc}\n"

            # Generate the RDF file to store
            rdf_filename = "concept_details.ttl"
            rdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], rdf_filename)
            with open(rdf_file_path, 'w') as rdf_file:
                rdf_file.write(rdf_content)

            # Save the annotated image
            if image:
                annotated_image_path = os.path.join(app.config['UPLOAD_FOLDER'], "annotated_image.jpg")
                image.save(annotated_image_path)

            return render_template("results.html", 
                                   detections=detections, 
                                   image_path=annotated_image_path, 
                                   concept_details=concept_details, 
                                   rdf_content=rdf_content,
                                   rdf_filename=rdf_filename)

    return render_template("index.html")



app.run(debug=True)
