from google.cloud import storage
import os
from pathlib import Path
from dotenv import load_dotenv


filepath = Path(__file__).resolve()
env_path = filepath.parent.parent / ".env"
env_file = load_dotenv(env_path)

BUCKET = os.environ.get("GCP_GCS_BUCKET", "default_bucket_name")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(filepath.parent.parent / "keys.json")

test = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

