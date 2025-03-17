# Object Classification, RDF Storage, and ConceptNet Integration

This repository showcases an integrated system for object classification using YOLO, semantic knowledge retrieval using ConceptNet, and RDF storage with Apache Jena Fuseki. The system processes images, extracts object labels, queries ConceptNet for semantic context, and stores the data as RDF triples in Fuseki.

## Features

* **Object Classification** : Uses YOLO to detect and classify objects in images.
* **Semantic Knowledge Retrieval** : Queries ConceptNet to enhance object understanding.
* **RDF Storage & Querying** : Stores structured knowledge in Apache Jena Fuseki and allows SPARQL queries.
* **Flask API** : Provides an interface for uploading images and retrieving RDF data.
* **SPARQL-based Data Visualization** : Fetches and displays stored RDF triples.

## Installation

### Prerequisites

* Python
* Docker (for running Apache Jena Fuseki)
* Flask
* OpenCV & YOLO

### Clone the Repository

```bash
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Apache Jena Fuseki

Run Fuseki using Docker:

```bash
docker run -d -p 3030:3030 --name fuseki stain/jena-fuseki
```

Alternatively, start Fuseki manually:

```bash
./fuseki-server --update --mem /dataset
```

## Usage

### 1. Start the Flask API

```bash
python app.py
```

### 2. Run a SPARQL Query on Fuseki

Example query to retrieve all triples:

```sparql
PREFIX ex: <http://example.org/>
SELECT ?subject ?predicate ?object WHERE {
    ?subject ?predicate ?object .
}
LIMIT 100
```

Run this in the Fuseki web UI at `http://localhost:3030/dataset.html`.
