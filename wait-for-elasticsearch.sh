#!/bin/bash

# Wait for Elasticsearch to be ready

host="localhost"
port="9200"
timeout=60
interval=5

echo "Waiting for Elasticsearch to be ready..."

while ! curl -s --fail -XGET "http://${host}:${port}" >/dev/null; do
    timeout=$((timeout - interval))
    if [ $timeout -le 0 ]; then
        echo "Timeout reached. Elasticsearch is not available."
        exit 1
    fi
    echo "Elasticsearch is not ready yet. Retrying in $interval seconds..."
    sleep $interval
done

echo "Elasticsearch is now ready."
