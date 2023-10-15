"""
Actions over GCP's Buckets
"""

import gcsfs

gcs = gcsfs.GCSFileSystem()
PATH_BUCKET = "gs://dmc-proyecto-big-data-24"
PATH_WORKLOAD = f"{PATH_BUCKET}/datalake/workload/FastAPI/csv"


def ls_bucket():
    """
    Returns:
        files: files in workload
    """
    files = gcs.ls(PATH_WORKLOAD)
    return files


def upload_file(file_name, data):
    """Upload file to Bucket

    Args:
        file_name (string)
        data (csv)
    """
    path = f"{PATH_WORKLOAD}/{file_name}"
    with gcs.open(path, "w") as file:
        file.write(data)
