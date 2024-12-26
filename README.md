Work description

In this work you need to first study the ConceptNet Knowledge graph.

Create your own RDF database (your own custom triple store) using one of the several open-source RDF triplestores in the list bellow to store the concepts and properties of the ConceptNet knowledge graph.

Implement the following logical program in python

Implement a Yolo classifier that takes as input an image of a daily living object and provides a vector of class names.

Transform the classification results into SPARQL Queries to extract from conceptnet the description of the image and store it in your RDF database.

Before storage check the consistency of your ontology using Pellet or another reasoner

How to manage the uncertainty in this case ?

The following triple stores are widely recognized for their production readiness and performance.

Apache Jena TDB:

- Description: Part of the Apache Jena framework, TDB is a robust triplestore that supports SPARQL and is designed for large datasets.
- Features: Supports RDF, RDFS, OWL, and SPARQL 1.1. It provides transaction support and can handle large-scale data.

Blazegraph:

- Description: Known for its high performance and scalability, Blazegraph is suitable for both small and large datasets.
- Features: Provides a full SPARQL 1.1 implementation, supports geospatial data, and offers graph analytics capabilities.

GraphDB:

Description: A highly scalable RDF triplestore with a focus on semantic graph data management.

Features: Supports reasoning, full-text search, and advanced analytics. It has a user-friendly interface and robust integration capabilities.

Fuseki:

- Description: Also part of the Apache Jena project, Fuseki is a SPARQL server that can run on top of TDB or other storage backends.
- Features: Provides a RESTful interface, supports SPARQL queries, and allows for easy deployment.

RDF4J:

- Description: A flexible framework for working with RDF data, RDF4J includes a triplestore that is suitable for various applications.
- Features: Supports transaction management, SPARQL 1.1, and can be embedded in Java applications.

Virtuoso (DBpedia)

Stardog
