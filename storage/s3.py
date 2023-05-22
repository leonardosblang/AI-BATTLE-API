import boto3
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from botocore.exceptions import NoCredentialsError

import json
import boto3
from botocore.exceptions import NoCredentialsError

class S3Manager:
    def __init__(self, config_file):
        with open(config_file) as json_file:
            config = json.load(json_file)
        self.bucket_name = config["bucket_name"]
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=config["aws_access_key_id"],
            aws_secret_access_key=config["aws_secret_access_key"],
            region_name=config["aws_region"]
        )
    def upload_image_to_s3(self, image_file, object_name):
        try:
            self.s3_client.upload_fileobj(
                image_file,
                self.bucket_name,
                object_name,
                ExtraArgs={"ContentType": "image/png"}
            )
            return True
        except NoCredentialsError:
            return False

    def download_image_from_s3(self, object_name, temp_file_path):
        try:
            with open(temp_file_path, "wb") as temp_file:
                self.s3_client.download_fileobj(self.bucket_name, object_name, temp_file)
            return True
        except NoCredentialsError:
            return False
