from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IcebergWithRestCatalog") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.my_catalog.catalog-impl", "org.apache.iceberg.rest.RESTCatalog") \
    .config("spark.sql.catalog.my_catalog.uri", "http://iceberg-rest:8181") \
    .config("spark.sql.catalog.my_catalog.warehouse", "s3a://iceberg/warehouse") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# Create namespace first
try:
    spark.sql("CREATE NAMESPACE IF NOT EXISTS my_catalog.db")
    print("Namespace 'db' created successfully")
except Exception as e:
    print(f"Error creating namespace: {e}")

# Create table
try:
    spark.sql("CREATE TABLE IF NOT EXISTS my_catalog.db.users (id INT, name STRING) USING iceberg")
    print("Table 'users' created successfully")
except Exception as e:
    print(f"Error creating table: {e}")

# Insert data
try:
    spark.sql("INSERT INTO my_catalog.db.users VALUES (1, 'Alice'), (2, 'Bob')")
    print("Data inserted successfully")
except Exception as e:
    print(f"Error inserting data: {e}")

# Query data
try:
    df = spark.sql("SELECT * FROM my_catalog.db.users")
    df.show()
except Exception as e:
    print(f"Error querying data: {e}")

spark.stop()