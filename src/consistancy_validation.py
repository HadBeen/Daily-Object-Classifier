from pyshacl import validate

def validate_rdf(rdf_file):
    conforms, results_graph, results_text = validate(data_graph=rdf_file)
    if not conforms:
        print("Ontology Inconsistent")
    return conforms
