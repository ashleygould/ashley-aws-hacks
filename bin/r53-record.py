#!/usr/bin/env python
"""
query record sets in a hosted zone by name or type

Usage:
    r53-record (-hv)
    r53-record [-p] [-t TYPE] [-n NAME] [-r REGION] DOMAINNAME



Options:
    -h, --help           Print usage message.
    -v, --version        Print version info.
    -t, --type TYPE      Type of DNS record.
    -n, --name NAME      Name of DNS record.
    -r, --region REGION  AWS region.
    -p, --private        Hosted zone is private
    DOMAINNAME           The DNS domain name of the hosted zone to query.

"""

import os
import json
import yaml
import boto3
from docopt import docopt


__version__ = '0.0.0'
DEFAULT_REGION = 'us-west-2'
TYPES = ['SOA', 'A', 'TXT', 'NS', 'CNAME', 'MX', 'NAPTR', 'PTR', 'SRV', 'SPF', 'AAAA', 'CAA']


def get_hosted_zone_id(domain_name, private_zone=False, region=DEFAULT_REGION):
    """
    Return the hosted zoned Id corresponding to 'domain_name'.
    """
    route53_client = boto3.client('route53', region_name=region)
    response = route53_client.list_hosted_zones()
    hosted_zones = response["HostedZones"]
    while response["IsTruncated"]:
        response = route53_client.list_hosted_zones(
            Marker=reponse["NextMarker"]
        )
        hosted_zones += response["HostedZones"]
    if not domain_name.endswith("."):
        domain_name += "."
    hosted_zone_ids = [
        zone['Id'] for zone in hosted_zones if
        zone['Name'] == domain_name and
        zone['Config']['PrivateZone'] is private_zone
    ]
    if len(hosted_zone_ids) > 1:
        raise RuntimeError(
            "Found multiple matching hosted zones: {}".format(cert_list)
        )
    if len(hosted_zone_ids) < 1:
        return None
    return hosted_zone_ids[0].split("/")[2]


def main():
    args = docopt(__doc__, version=__version__)
    print(args)

    if not args['--region']:
        region = DEFAULT_REGION
    else:
        region = args['--region']

    if args['--type'] and not args['--type'] in TYPES:
        raise ValueError(
            "'TYPE' must be one of {}".format(TYPES)
        )

    client = boto3.client('route53', region_name=region)
    hosted_zone_id = get_hosted_zone_id(args['DOMAINNAME'], args['--private'], region)
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

