#!/bin/bash
# Pull the Docker image
docker pull stain/jena-fuseki

# Run the Docker container
docker run -d -p 3030:3030 --name fuseki stain/jena-fuseki

echo "Apache Jena Fuseki is now running at http://localhost:3030/"
