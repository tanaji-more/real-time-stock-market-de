import os
import boto3
from pathlib import Path
import snowflake.connector
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv

#root path
# env_path = Path(__file__).resolve().parent.parent / ".env"
env_path = Path("/opt/airflow/dags/.env")


# load .env file
load_dotenv(dotenv_path=env_path)

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET = os.getenv("BUCKET")
#LOCAL_DIR = os.getenv("LOCAL_DIR")
LOCAL_DIR = os.getenv("LOCAL_DIR", "/opt/airflow/data")


SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT =  os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

def download_from_minio():
    os.makedirs(LOCAL_DIR, exist_ok = True)
    s3 = boto3.client(
        "s3",
        endpoint_url = MINIO_ENDPOINT,
        aws_access_key_id = MINIO_ACCESS_KEY,
        aws_secret_access_key = MINIO_SECRET_KEY
    )

    objects = s3.list_objects_v2(Bucket = BUCKET).get("Contents", [])
    local_files = []
    for obj in objects:
        key = obj["Key"]
        local_file = os.path.join(LOCAL_DIR, os.path.basename(key))
        s3.download_file(BUCKET, key, local_file)
        print(f"Downloaded {key} -> {local_file}")
        local_files.append(local_file)
    return local_files

def load_to_snowflake(**kwargs):
    local_files = kwargs['ti'].xcom_pull(task_ids = 'download_minio')
    if not local_files:
        print("No files to load")
        return

    conn = snowflake.connector.connect(
        user = SNOWFLAKE_USER,
        password = SNOWFLAKE_PASSWORD,
        account = SNOWFLAKE_ACCOUNT,
        warehouse = SNOWFLAKE_WAREHOUSE,
        database = SNOWFLAKE_DB,
        schema = SNOWFLAKE_SCHEMA
    )

    cur = conn.cursor()

    for f in local_files:
        cur.execute(f"PUT file://{f} @%bronze_stock_quotes_raw")
        print(f"Uploaded {f} to Snowflake stage")

    cur.execute("""
        COPY INTO bronze_stock_quotes_raw
        FROM @%bronze_stock_quotes_raw
        FILE_FORMAT = (TYPE = JSON)
    """)

    print("COPY INTO executed")

    cur.close()
    conn.close()

default_args = {
    "owner" : "ariflow",
    "depends_on_past" : False,
    "start_date" : datetime(2026, 1, 12),
    "retries" : 1,
    "retry_delay" : timedelta(minutes=5)
}

with DAG(
    "minio_to_snowflake",
    default_args = default_args,
    schedule_interval = "*/1 * * * *", # every one minutes
    catchup = False
) as dag:
    task1 = PythonOperator(
        task_id = "download_minio",
        python_callable = download_from_minio,
    )

    task2 = PythonOperator(
        task_id = "load_snowflake",
        python_callable = load_to_snowflake,
        provide_context = True
    )

    task1 >> task2
