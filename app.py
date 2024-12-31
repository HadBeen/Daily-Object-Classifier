from flask import Flask, request, render_template , send_from_directory
from src.object_classifier import classify_image
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL
from requests.auth import HTTPBasicAuth
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

        # Define namespaces
        ex = Namespace("http://example.org/")
        g.bind("ex", ex)

        concept_uri = ex[concept]

        # Add the main concept as a class
        g.add((concept_uri, RDF.type, OWL.Class))
        g.add((concept_uri, RDFS.label, Literal(concept)))

        if 'edges' in data:
            for edge in data['edges']:
                # Extract details from each edge
                start_node = edge.get('start', {}).get('label', None)
                end_node = edge.get('end', {}).get('label', None)
                relation = edge.get('rel', {}).get('label', None)

                if start_node and end_node and relation:
                    start_uri = ex[start_node.replace(" ", "_")]
                    end_uri = ex[end_node.replace(" ", "_")]
                    relation_uri = ex[relation.replace(" ", "_")]

                    # Add nodes and relations to the graph
                    g.add((start_uri, RDFS.label, Literal(start_node)))
                    g.add((end_uri, RDFS.label, Literal(end_node)))
                    g.add((relation_uri, RDFS.label, Literal(relation)))

                    # Create relationships in RDF
                    g.add((start_uri, relation_uri, end_uri))

        # Save RDF file to the server's directory
        rdf_filename = f"{concept}_description.ttl"
        rdf_file_path = os.path.join(app.config['UPLOAD_FOLDER_RDF'], rdf_filename)
        g.serialize(destination=rdf_file_path, format="turtle")

        return rdf_file_path, rdf_filename
    else:
        return None, "Error fetching data"




def upload_to_fuseki(file_path, fuseki_url, username=None, password=None):
        
        print("file path",file_path)
        with open(file_path, 'r', encoding='utf-8') as rdf_file:
            data = rdf_file.read()

            headers = {'Content-Type': 'text/turtle;charset=utf-8'}
            fuseki_url = 'http://localhost:3030/daily_objects/data'  # Replace with your dataset URL
            response = requests.post(fuseki_url, data=data, headers=headers, auth=HTTPBasicAuth(username, password))

            if response.status_code in [200, 204]:
                print("RDF data uploaded successfully.")
            else:
                print(f"Failed to upload RDF data. Status code: {response.status_code}")
                print(response.text)



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

            print("li nmdo as param",rdf_file_path)
            upload_to_fuseki(descriptions[0], "http://localhost:3030/#/dataset/daily_objects", "admin", "C17MxdOss8cVBA5")
            print(descriptions[0])
            print('doooonnnee')

            return render_template("results.html", 
                                   detections=detections, 
                                   image_path=annotated_image_path, 
                                   concept_details=concept_details, 
                                   rdf_content=rdf_content,
                                   rdf_filename=rdf_filename)

    return render_template("index.html")



app.run(debug=True)
