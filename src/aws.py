import boto3
from werkzeug.utils import secure_filename
import os
import uuid


class AWS():

    # starting the sdk client
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def read_image(self, obj_key: str):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=obj_key)
        image_data = response['Body'].read()
        return image_data

    def upload_image(self, img_file, filename):
        response = self.s3.upload_file(
            filename,
            self.bucket_name,
            img_file,
        )

    def change_image(self, img_file):
        unique_id = str(uuid.uuid4().hex)
        original_filename = secure_filename(img_file.filename)
        filename, extension = original_filename.rsplit('.', 1)
        new_filename = f"{filename}_{unique_id}.{extension}"
        img_file.save(f"temp/{new_filename}")
        # calls function to upload s3
        self.upload_image(new_filename, f"temp/{new_filename}")

        os.remove(f"temp/{new_filename}")

        return new_filename


class AWS_S3(AWS):
    def __init__(self,) -> None:
        super().__init__('aqo-balloon-gallery')
        self.keys = []

# utilize the self.keys to not get the same object twice

    def read_all_keys(self):
        response = self.s3.get_object(Bucket=self.bucket_name)
        if 'Contents' in response:
            object_keys = [obj['Key'] for obj in response['Contents']]
            return object_keys
        return []
