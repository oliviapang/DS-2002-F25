#!/bin/bash
set -e

FILE=$1
BUCKET=$2
EXPIRATION=$3

echo "Uploading $FILE"
aws s3 cp $FILE s3://$BUCKET/

URL=$(aws s3 presign "s3://$BUCKET/$FILE" --expires-in "$EXPIRATION")

echo "Presigned URL: $URL"
