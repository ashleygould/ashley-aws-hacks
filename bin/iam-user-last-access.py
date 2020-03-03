#!/usr/bin/env python

import io
import sys
import csv
from datetime import datetime, timezone, timedelta


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

def str2datetime(date_str):
    time_format = "%Y-%m-%dT%H:%M:%S+00:00"
    return datetime.strptime(date_str, time_format)

def is_more_than(days, date_str):
    return datetime.now() - str2datetime(date_str) > timedelta(days=int(days))

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--days-since',
    required=False,
    help='Report only users whose last access was more than X number of days ago.'
)
@click.option('--never',
    is_flag=True,
    default=False,
    help='Report only IAM users who have never logged in  at all.'
)
def main(days_since, never):
    #print(days_since, never)

    user_info = credentials_report()

    if never:
        pw_never_used = [user for user in user_info if not "password_last_used" in user]
        no_access_keys = [user for user in user_info if not "access_key_1_active" in user
                and not "access_key_2_active" in user]
        never_used = [user["Arn"] for user in pw_never_used if user in no_access_keys]

        key = "User never logged in"
        print(yamlfmt({key: never_used}))

    if days_since is not None:
        pw_last_used_more_than = [user["Arn"] for user in user_info
            if "password_last_used" in user
            and is_more_than(days_since, user["password_last_used"])
            #and datetime.now() - str2datetime(user["password_last_used"]) > timedelta(days=int(more_than))
        ]


        key = "No console login for over {} days".format(days_since)
        print(yamlfmt({key: pw_last_used_more_than}))




if __name__ == "__main__":
    main()
