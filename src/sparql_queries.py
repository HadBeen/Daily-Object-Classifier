from SPARQLWrapper import SPARQLWrapper, JSON

def fetch_concept_details(concept):
    sparql = SPARQLWrapper("https://conceptnet.io/sparql")
    sparql.setQuery(f"""
        SELECT ?property ?value WHERE {{
            <http://conceptnet.io/c/{concept}> ?property ?value
        }}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results
