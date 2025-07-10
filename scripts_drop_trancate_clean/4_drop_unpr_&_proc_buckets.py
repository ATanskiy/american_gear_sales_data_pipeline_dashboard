import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

# Connect to MinIO
s3 = boto3.client(
    's3',
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY")
)

BUCKETS = ["unprocessed-data", "processed-data"]

def delete_bucket_completely(bucket):
    try:
        # Check if bucket exists
        s3.head_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response['Error']['Code'] in ("404", "NoSuchBucket"):
            print(f"❌ Bucket '{bucket}' does not exist.")
            return
        else:
            print(f"⚠️ Error checking bucket '{bucket}': {e.response['Error']['Message']}")
            return

    try:
        # Delete all objects
        response = s3.list_objects_v2(Bucket=bucket)
        objects = [{'Key': obj['Key']} for obj in response.get('Contents', [])]
        if objects:
            s3.delete_objects(Bucket=bucket, Delete={'Objects': objects})
            print(f"🗑️ Deleted {len(objects)} objects from bucket '{bucket}'.")
        else:
            print(f"🧺 Bucket '{bucket}' was already empty.")

        # Delete the bucket
        s3.delete_bucket(Bucket=bucket)
        print(f"❌ Deleted bucket '{bucket}'.")
    except ClientError as e:
        print(f"⚠️ Error deleting '{bucket}': {e.response['Error']['Message']}")

if __name__ == "__main__":
    for bucket in BUCKETS:
        delete_bucket_completely(bucket)