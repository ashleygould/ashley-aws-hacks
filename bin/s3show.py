#!/usr/bin/env python
"""Describe s3 bucket configurations.
List all objects in a versioned bucket."""
import sys
import boto3
import yaml

def yprint(obj):
    if obj:
        print(yaml.dump(obj, default_flow_style=False).rstrip())


if len(sys.argv) <= 1:
    print('provide a bucket name')
    sys.exit(1)

bucket_name = sys.argv[1]
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
bucket.load()
if not bucket.creation_date:
    print('no such bucket')
    sys.exit(1)

print('Number of objects in bucket: {}'.format(sum(1 for _ in bucket.objects.all())))

try:
    bucket.Acl().load()
    print('\nAcl for bucket {}:'.format(bucket.name))
    yprint(bucket.Acl().owner)
    yprint(bucket.Acl().grants)
except:
    pass

try:
    bucket.Cors().load()
    print('\nCors for bucket {}:'.format(bucket.name))
    yprint(bucket.Cors().rules)
except:
    pass

try:
    bucket.Lifecycle().load()
    print('\nLifecycle for bucket {}:'.format(bucket.name))
    yprint(bucket.Lifecycle().rules)
except:
    pass

try:
    bucket.Logging().load()
    print('\nLogging for bucket {}:'.format(bucket.name))
    yprint(bucket.Logging().logging_enabled)
except:
    pass

try:
    bucket.Notification().load()
    print('\nNotification for bucket {}:'.format(bucket.name))
    yprint(bucket.Notification().lambda_function_configurations)
    yprint(bucket.Notification().queue_configurations)
    yprint(bucket.Notification().topic_configurations)
except:
    pass

try:
    bucket.Policy().load()
    print('\nPolicy for bucket {}:'.format(bucket.name))
    yprint(bucket.Policy().policy)
except:
    pass

try:
    bucket.RequestPayment().load()
    print('\nRequestPayment for bucket {}:'.format(bucket.name))
    yprint(bucket.RequestPayment().payer)
except:
    pass

try:
    bucket.Tagging().load()
    print('\nTagging for bucket {}:'.format(bucket.name))
    yprint(bucket.Tagging().tag_set)
except:
    pass

print('Number of versions in bucket: {}'.format(sum(1 for _ in bucket.object_versions.all())))
try:
    bucket.Versioning().load()
    print('\nVersioning for bucket {}:'.format(bucket.name))
    yprint(bucket.Versioning().mfa_delete)
    yprint(bucket.Versioning().status)
    print('Number of versions in bucket: {}'.format(sum(1 for _ in bucket.object_versions.all())))
except:
    pass

try:
    bucket.Website().load()
    print('\nWebsite for bucket {}:'.format(bucket.name))
    yprint(bucket.Website().error_document)
    yprint(bucket.Website().index_document)
    yprint(bucket.Website().redirect_all_requests_to)
    yprint(bucket.Website().routing_rules)
except:
    pass





#for objv in bucket.object_versions.all():
#    print("deleting {}".format(objv))

#bucket.object_versions.delete()
#bucket.delete()
