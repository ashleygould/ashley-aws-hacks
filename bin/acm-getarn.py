#!/bin/env python

import sys
import boto3

if len(sys.argv) <= 1:
    print('provide a certificate domain name')
    sys.exit(1)
domain = sys.argv[1]

acm_client = boto3.client('acm')
response = acm_client.list_certificates()
certlist = response['CertificateSummaryList']
if 'NextToken' in response:
    while response['NextToken']:
        response = acm_client.list_certificates(NextToken=response['NextToken'])
        certlist += response['CertificateSummaryList']
certarn = [cert['CertificateArn'] for cert in certlist if cert['DomainName'] == domain]
if len(certarn) == 1:
    print(certarn[0])
