# Use the official Elasticsearch Docker image
FROM docker.elastic.co/elasticsearch/elasticsearch:8.12.2

# Expose Elasticsearch port
EXPOSE 9200

# Set environment variables
ENV discovery.type=single-node
ENV xpack.security.enabled=false

# Switch to root user to perform privileged operations
USER root

# Create missing directory
RUN mkdir -p /var/lib/apt/lists/partial

# Install Python and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions for Elasticsearch data directory
RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/data

# Set the working directory in the container
WORKDIR /app

# Copy the required files for the Dash app
COPY app.py footer.py requirements.txt robots.txt sitemap.xml ./
COPY assets assets
COPY pages pages

# Install Python dependencies for the Dash app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script to wait for Elasticsearch
COPY wait-for-elasticsearch.sh /usr/local/bin/wait-for-elasticsearch.sh

# Set execute permissions for the script
RUN chmod +x /usr/local/bin/wait-for-elasticsearch.sh

# Switch to the non-root user for running Elasticsearch
USER elasticsearch

# Start Elasticsearch and then start Dash app after Elasticsearch is ready
CMD ["bash", "-c", "elasticsearch & /usr/local/bin/wait-for-elasticsearch.sh && python3 app.py"]
