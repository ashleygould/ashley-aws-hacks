#!/usr/bin/env python

import io
import sys
import csv
import boto3
from botocore.exceptions import ClientError
import click
import yaml


def yamlfmt(dict_obj):
    """Convert a dictionary object into a yaml formated string"""
    return yaml.dump(dict_obj, default_flow_style=False)


def credentials_report():

    messages = []
    iam_client = boto3.client('iam')
    try:
        response = iam_client.get_credential_report()
    except Exception as e:
        response = iam_client.generate_credential_report()
        messages.append(yamlfmt(response))
        return messages

    report_file_object = io.StringIO(response['Content'].decode())
    reader = csv.DictReader(report_file_object)
    user_info = []
    for row in reader:
        user = dict()
        for key in reader.fieldnames:
            user['UserName'] = row['user']
            user['Arn'] = row['arn']
            if (key not in ['user', 'arn'] and
                    row[key] not in ['N/A', 'not_supported', 'no_information', 'false']):
                user[key] = row[key]
        user_info.append(user)

    return user_info


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--more-than',
    required=False,
    help='Report only users whose last access was more than X number of days ago.'
)
@click.option('--less-than',
    required=False,
    help='Report only users whose last access was less than X number of days ago.'
)
def main(more_than, less_than):
    print(more_than, less_than)

    user_info = credentials_report()
    print(yamlfmt(dict(Users=user_info)))


if __name__ == "__main__":
    main()
