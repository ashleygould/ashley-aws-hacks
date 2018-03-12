#!/usr/bin/env python
"""Delete all objects in a versioned bucket and delete the bucket"""
import sys
import boto3

if len(sys.argv) <= 1:
    print('provide a bucket name')
    sys.exit(1)

bucket_name = sys.argv[1]
print('deleting bucket {}'.format(bucket_name))
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
bucket.objects.delete()
bucket.object_versions.delete()
bucket.delete()
