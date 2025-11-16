#!/usr/bin/env python3
# this script works when I use winpty python upload.py, but had some issues when I tried
# running it with ./upload.py. I think the issues are Bash related

import boto3
import requests

url = input("Enter URL: ")
bucket_name = input("Enter bucket name: ")
object_name = input("Enter object name: ")
expires_in = int(input ("Expires in: "))

def download_file(url, file_path):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")

download_file(url, object_name)

s3 = boto3.client('s3', region_name="us-east-1")


with open(object_name, 'rb') as data:
    resp = s3.put_object(
        Body=data,
        Bucket=bucket_name,
        Key=object_name
)

response = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': object_name},
    ExpiresIn=expires_in
)

print(response)
