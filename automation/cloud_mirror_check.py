#!/usr/bin/env python3
"""
cloud_mirror_check.py
Checks whether local archives and results match with those in a GCS bucket.
"""
import os
from google.cloud import storage
from rich.console import Console
from rich.table import Table

console = Console()

def check_bucket(bucket_name, local_dir="archives"):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = {blob.name for blob in bucket.list_blobs()}
    locals = {f for f in os.listdir(local_dir) if f.endswith(".zip")}
    missing = locals - blobs
    extra = blobs - locals

    table = Table(title="Cloud Mirror Audit")
    table.add_column("Status", justify="center")
    table.add_column("File")
    for f in missing:
        table.add_row("[yellow]Missing in Cloud[/]", f)
    for f in extra:
        table.add_row("[red]Extra in Cloud[/]", f)

    console.print(table)
    if not missing and not extra:
        console.print("[green]✅ Cloud mirror is in sync.[/]")
    else:
        console.print("[cyan]Manual sync required via upload_to_gcs.py[/]")

if __name__ == "__main__":
    bucket = os.getenv("SRCL_GCS_BUCKET", "your-bucket-name")
    check_bucket(bucket)
