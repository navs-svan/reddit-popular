from google.cloud import storage, bigquery
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


def upload_to_bq(bq_client: bigquery.Client, dataset, table_name, bucket_uri):
    """
    REF: https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet
    """
    print(f"Uploading {bucket_uri}")
    table_id = f"{dataset}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition="WRITE_APPEND",
    )

    load_job = bq_client.load_table_from_uri(
        bucket_uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = bq_client.get_table(table_id)

    print("Loaded {} rows.".format(destination_table.num_rows))


def retrieve_gcs_files_uri(bcs_client: storage.Client, bucket, date):

    blobs = bcs_client.list_blobs(bucket, prefix=f"{date}/")
    for blob in blobs:
        yield get_blob_uri(blob)


def get_blob_uri(gcs_blob):
    return f"gs://{gcs_blob.bucket.name}/{gcs_blob.name}"


if __name__ == "__main__":
    filepath = Path(__file__).resolve()
    env_path = filepath.parent.parent / ".env"
    env_file = load_dotenv(env_path)

    BUCKET = os.environ.get("GCP_GCS_BUCKET", "bucket_name")
    DATASET = os.environ.get("GCP_BQ_DATASET", "dataset_name")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
        filepath.parent.parent / "keys.json"
    )

    bq_client = bigquery.Client()
    storage_client = storage.Client()
    cur_date = datetime.today().strftime("%Y-%m-%d")

    for uri in retrieve_gcs_files_uri(storage_client, BUCKET, cur_date):
        country = uri.split("/")[-1].split("_")[0]
        upload_to_bq(bq_client, DATASET, country, uri)
