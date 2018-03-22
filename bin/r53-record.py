#!/usr/bin/env python
"""
query record sets in a hosted zone by name or type

Usage:
    r53-record (-hv)
    r53-record [-t TYPE] [-n NAME] [-r REGION] DOMAINNAME



Options:
    -h, --help           Print usage message.
    -v, --version        Print version info.
    -t, --type TYPE      Type of DNS record.
    -n, --name NAME      Name of DNS record.
    -r, --region REGION  AWS region.
    DOMAINNAME           The DNS domain name of the hosted zone to query.

"""

import os
import json
import yaml
import boto3
from docopt import docopt
from sceptremods.util.acm import get_hosted_zone_id

__version__ = '0.0.0'
DEFAULT_REGION = 'us-west-2'
TYPES = ['SOA', 'A', 'TXT', 'NS', 'CNAME', 'MX', 'NAPTR', 'PTR', 'SRV', 'SPF', 'AAAA', 'CAA']

def main():
    args = docopt(__doc__, version=__version__)
    #print(args)

    if not args['--region']:
        region = DEFAULT_REGION
    else:
        region = args['--region']

    if args['--type'] and not args['--type'] in TYPES:
        raise ValueError(
            "'TYPE' must be one of {}".format(TYPES)
        )

    client = boto3.client('route53', region_name=region)
    hosted_zone_id = get_hosted_zone_id(args['DOMAINNAME'], region)
    #print(hosted_zone_id)

    response = client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    records = response['ResourceRecordSets']
    if 'IsTruncated' in response:
        while response['IsTruncated']:
            response = client.list_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                StartRecordName=response['NextRecordName'],
                StartRecordType=response['NextRecordType'],
            )
            records.append(response['ResourceRecordSets'])

    if args['--type']:
        records = [r for r in records if r['Type'] == args['--type']]

    if args['--name']:
        records = [r for r in records 
            if args['--name'] in r['Name']
            and r['Name'].split('.')[0] == args['--name'].split('.')[0]
        ]
    print(yaml.dump(records, default_flow_style=False).rstrip())

if __name__ == '__main__':
    main()

