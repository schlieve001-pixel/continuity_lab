#!/usr/bin/env python3
"""
SRCL Elite – Cloud Upload Agent
Uploads results to GCS with metadata and checksum verification.
"""

import os, hashlib
from google.cloud import storage

BUCKET_NAME = "srcl-lab-data"
RESULTS_PATH = "results_montecarlo_v3"

def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    for root, _, files in os.walk(RESULTS_PATH):
        for file in files:
            path = os.path.join(root, file)
            blob = bucket.blob(path)
            checksum = sha256sum(path)
            blob.metadata = {"checksum": checksum}
            blob.upload_from_filename(path)
            print(f"☁️ Uploaded {path} with checksum {checksum[:8]}")

if __name__ == "__main__":
    upload_to_gcs()
