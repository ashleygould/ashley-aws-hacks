#!/usr/bin/env python
"""
add cname record set to hostedzone

Usage:
    r53-cname (-hv)
    r53-cname ACTION DOMAINNAME CNAME TARGET [-r REGION]

Options:
    -h, --help           Print usage message.
    -v, --version        Print version info.
    -r, --region REGION  AWS region for initialized project.

"""

import os
import json

import boto3
from docopt import docopt
from sceptremods.util.acm import get_hosted_zone_id

__version__ = '0.0.0'
DEFAULT_REGION = 'us-west-2'
ACTIONS = {
    'create': 'CREATE',
    'update': 'UPSERT',
    'delete': 'DELETE',
}

def main():
    args = docopt(__doc__, version=__version__)
    print(args)

    if not args['--region']:
        region = DEFAULT_REGION
    else:
        region = args['--region']

    if not args['ACTION'] in ACTIONS.keys():
        raise ValueError(
            "'ACTION' must be one of {}".format(ACTIONS.keys())
        )


    client = boto3.client('route53', region_name=region)
    hosted_zone_id = get_hosted_zone_id(args['DOMAINNAME'], region)
    print(hosted_zone_id)
    change_batch ={
        'Comment': 'cname resource record',
        'Changes': [
            {
                'Action': ACTIONS[args['ACTION']],
                'ResourceRecordSet': {
                    'Name': args['CNAME'],
                    'Type': 'CNAME',
                    'TTL': 300,
                    'ResourceRecords': [{'Value': args['TARGET']}],
                }
            }
        ]
    }
    print('Submitting changes: {}\n'.format(change_batch))
    response = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch=change_batch,
    )
    print(response['ChangeInfo'])


if __name__ == '__main__':
    main()

