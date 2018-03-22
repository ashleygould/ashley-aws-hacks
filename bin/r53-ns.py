#!/usr/bin/env python
"""
add delegation record set for new subdomain hosted zone to parent domain
hosted zone

from subdomain account:
get child hosted zone id from subdomainname
list record sets for zone
grab the record set with Type: NS

assume role into parent domain account
get parent hosted zone id from domainname
run change record set to upsert child zone's NS record set

Usage:
    r53-ns (-hv)
    r53-ns get [-r REGION] DOMAINNAME -f RECORDSET
    r53-ns set [-r REGION] DOMAINNAME -f RECORDSET

Options:
    -h, --help           Print usage message.
    -v, --version        Print version info.
    -r, --region REGION  AWS region for initialized project.
    -f,  --file RECORDSET  filename of the ns record set.

"""

import os
import json

import boto3
from docopt import docopt
from sceptremods.util.acm import get_hosted_zone_id

__version__ = '0.0.0'
DEFAULT_REGION = 'us-west-2'

def main():
    args = docopt(__doc__, version=__version__)
    #print(args)

    if not args['--region']:
        region = DEFAULT_REGION
    else:
        region = args['--region']

    if args['get']:
        client = boto3.client('route53', region_name=region)
        hosted_zone_id = get_hosted_zone_id(args['DOMAINNAME'], region)
        #print(hosted_zone_id)
        ns_record_set = client.list_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            StartRecordName=args['DOMAINNAME'],
            StartRecordType='NS',
        )['ResourceRecordSets'][0]
        #print(json.dumps(ns_record_set))
        with open(args['RECORDSET'], 'w') as fh:
            json.dump(ns_record_set, fh)

    if args['set']:
        client = boto3.client('route53', region_name=region)
        hosted_zone_id = get_hosted_zone_id(args['DOMAINNAME'], region)
        #print(hosted_zone_id)
        with open(args['RECORDSET'], 'r') as fh:
            ns_record_set = json.load(fh)
        #print(ns_record_set)
        change_batch ={
            'Comment': 'ns resource record',
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': ns_record_set['Name'],
                        'Type': ns_record_set['Type'],
                        'TTL': 300,
                        'ResourceRecords': ns_record_set['ResourceRecords'],
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

