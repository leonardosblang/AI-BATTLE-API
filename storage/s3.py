import os

import boto3
from PIL import Image
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

            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=3600  # set the URL to expire in 1 hour
            )

            return presigned_url

        except NoCredentialsError:
            return False

    def download_image_from_s3(self, object_name, user, card_num):
        try:
            # Check the extension of the file and create the temp file path accordingly
            ext = os.path.splitext(object_name)[1]
            temp_file_path = f'temp_{user}_card{card_num}{ext}'

            with open(temp_file_path, "wb") as temp_file:
                self.s3_client.download_fileobj(self.bucket_name, object_name, temp_file)

            # Check if the file is in a format that PIL can open
            Image.open(temp_file_path)

            return temp_file_path  # return the path of the downloaded image
        except NoCredentialsError:
            return False
        except Exception as e:
            print(f"Error downloading {object_name} from S3: {e}")
            return False

