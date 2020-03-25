#!/bin/env python
'''
revoke all ingress and egress rules attached to the given security group.
If security group has assigned resources, do nothing
'''

import sys
import boto3

if len(sys.argv) <= 1:
    print('provide a security group id')
    sys.exit(1)
group_id = sys.argv[1]

ec2_client = boto3.client('ec2')
response = ec2_client.describe_network_interfaces(
    Filters=[{
        'Name': 'group-id',
        'Values': [group_id]
    }],
)
if response['NetworkInterfaces']:
    sys.exit('sg has assigned resources')

ec2 = boto3.resource('ec2')
sg = ec2.SecurityGroup(group_id)
sg.load()

ip_permissions = sg.ip_permissions
if ip_permissions:
    print('revoking ingress rules:')
    print(ip_permissions)
    response = sg.revoke_ingress(
        IpPermissions=ip_permissions
    )

ip_permissions_egress = sg.ip_permissions_egress
if ip_permissions_egress:
    print('revoking egress rules:')
    print(ip_permissions_egress)
    response = sg.revoke_egress(
        IpPermissions=ip_permissions_egress
    )
