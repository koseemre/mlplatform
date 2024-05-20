from enum import Enum

class FileLocationType(Enum):
    FILE_SYSTEM = "file_system"
    CLOUD_GCP_BUCKET = "cloud_gcp_bucket"
    CLOUD_S3 = "cloud_s3"