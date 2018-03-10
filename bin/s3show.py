#!/usr/bin/env python
"""Describe s3 bucket configurations."""
import sys
import boto3
import yaml
import json


def yprint(obj):
    if obj:
        print(yaml.dump(obj, default_flow_style=False).rstrip())


def subresource_printer(bucket, subresource_name, attributes, attribute_fn=[]):
    print('\n{}:'.format(subresource_name))
    sub = eval('bucket.' + subresource_name + '()')
    try:
        sub.load()
        for attr in attributes:
            yprint(eval('sub.' + attr))
        for fn in attribute_fn:
            fn()
    except:
        return None


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


print('Report for bucket {}\n'.format(bucket.name))
print('Creation date: {}'.format(bucket.creation_date))
print('Object count: {}'.format(sum(1 for _ in bucket.objects.all())))
if bucket.Versioning().status:
    print('Versioned object count: {}'.format(
        sum(1 for _ in bucket.object_versions.all())
    ))

subresource_printer(bucket, 'Acl', ['owner', 'grants'])
subresource_printer(bucket, 'Cors', ['cors_rules'])
subresource_printer(bucket, 'Lifecycle', ['rules'])
subresource_printer(bucket, 'LifecycleConfiguration', ['rules'])
subresource_printer(bucket, 'Logging', ['logging_enabled'])
subresource_printer(bucket, 'Notification', [
    'lambda_function_configurations',
    'queue_configurations', 
    'topic_configurations'
])
subresource_printer(bucket, 'Policy', list(), [
    lambda : yprint(json.loads(bucket.Policy().policy))
])
subresource_printer(bucket, 'RequestPayment', ['payer'])
subresource_printer(bucket, 'Tagging', ['tag_set'])
subresource_printer(bucket, 'Versioning', ['mfa_delete', 'status'])
subresource_printer(bucket, 'Website', [
    'error_document',
    'index_document',
    'redirect_all_requests_to',
    'routing_rules',
])
