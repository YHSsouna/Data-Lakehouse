from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 7, 24),
}

with DAG('spark_iceberg_job', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    run_spark_job = BashOperator(
        task_id='run_spark_job',
        bash_command="""
        /opt/bitnami/spark/bin/spark-submit \
        --master spark://spark:7077 \
        --packages org.apache.iceberg:iceberg-spark-runtime-3.2_2.12:1.2.1,org.postgresql:postgresql:42.6.0 \
        /tmp/spark-events/test.py
        """
    )
