#!/bin/sh
set -e

# Wait for MinIO to be ready
until mc alias set minio http://minio:9000 admin password; do
  echo "Waiting for MinIO..."
  sleep 3
done

echo "MinIO ready, listing metadata files..."

# Find all metadata.json files in MinIO bucket
metadata_files=$(mc find minio/warehouse/warehouse --name '*.metadata.json')

for metadata in $metadata_files; do
  namespace=$(echo "$metadata" | cut -d '/' -f 5)
  table=$(echo "$metadata" | cut -d '/' -f 6)
  metadata_file=$(basename "$metadata")

  table_name="$namespace.$table"
  s3_path="s3://warehouse/warehouse/$namespace/$table/metadata/$metadata_file"

  echo "Registering table $table_name from $s3_path"

  # Use the Iceberg REST API to register table (adjust if your API differs)
  curl -X POST http://localhost:8181/v1/tables \
    -H "Content-Type: application/json" \
    -d '{
      "namespace": "'"$namespace"'",
      "name": "'"$table"'",
      "metadata_location": "'"$s3_path"'"
    }' || echo "Warning: registration might have failed or table exists"
done

echo "All tables registered. Starting Iceberg REST service..."

# Start the original Iceberg REST server process
exec java -jar /opt/iceberg/iceberg-rest.jar
