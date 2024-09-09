from google.cloud import storage
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


if __name__ == "__main__":

    filepath = Path(__file__).resolve()
    env_path = filepath.parent.parent / ".env"
    env_file = load_dotenv(env_path)

    BUCKET = os.environ.get("GCP_GCS_BUCKET", "default_bucket_name")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
        filepath.parent.parent / "keys.json"
    )

    cur_date = datetime.today().strftime("%Y-%m-%d")

    test = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    pathlist = (filepath.parent / "local_data").glob("*.parquet")
    for path in pathlist:
        upload_to_gcs(BUCKET, f"{cur_date}/{str(path.name)}", str(path))

        os.remove(path)
