import requests
def fetch_concept_details(concept):
    # ConceptNet API URL
    base_url = "http://api.conceptnet.io/c/en/"
    
    # Format the concept properly for the API call
    concept = concept.replace(" ", "_").lower()  # Convert to lowercase and replace spaces with underscores

    # Make the API call to ConceptNet
    response = requests.get(f"{base_url}{concept}")
    
    if response.status_code == 200:
        data = response.json()
        
        # Check for related concepts and return a brief description
        if 'edges' in data:
            descriptions = []
            for edge in data['edges']:
                # Extracting the relationship and related concept
                # Access the 'label' from the 'end' dictionary, not 'properties'
                if 'end' in edge and 'label' in edge['end']:
                    descriptions.append(edge['end']['label'])
            return descriptions
        else:
            return ["No related concepts found"]
    else:
        return [f"Error fetching data for {concept}"]