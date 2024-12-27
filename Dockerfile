FROM openjdk:11-jdk-slim

WORKDIR /fuseki

COPY --from=apache/jena-fuseki /fuseki /fuseki

EXPOSE 3030

ENTRYPOINT ["java", "-Xmx512M", "-Xms512M", "-jar", "fuseki-server.jar"]