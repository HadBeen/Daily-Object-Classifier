from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

def store_triples(concept, data):
    graph = Graph()
    NS = Namespace("http://example.org/")
    concept_node = URIRef(NS[concept])
    for prop, value in data.items():
        graph.add((concept_node, URIRef(NS[prop]), Literal(value)))
    graph.serialize("rdf_storage/concepts.rdf", format="xml")
