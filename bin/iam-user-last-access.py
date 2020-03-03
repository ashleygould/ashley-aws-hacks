#!/usr/bin/env python
'''

find users with obsolete credentials:

    - user has no password and no access keys

    - user is more than 30 days old but has never logged in

    - user has not logged in for over X number of days


'''

import io
import sys
import csv
from datetime import datetime, timezone, timedelta


import boto3
from botocore.exceptions import ClientError
import click
import yaml

NEW_USER_GRACE_PERIOD = 30


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

def is_less_than(days, date_str):
    return datetime.now() - str2datetime(date_str) < timedelta(days=int(days))


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--days-since',
    required=False,
    default=365,
    help='Report only users whose last access was more than X number of days ago.'
)
def main(days_since):
    #print(days_since)

    user_info = credentials_report()
    #print(yamlfmt(user_info))
    print(len(user_info))

    # user is brand new
    new_users = []
    for user in user_info:
        if is_less_than(NEW_USER_GRACE_PERIOD, user["user_creation_time"]):
            new_users.append(user_info.remove(user))

    print(len(new_users))
    print(len(user_info))

    # user has no password and no access keys

    pw_not_enabled = []
    for user in user_info:
        if not "password_enabled" in user:
            pw_not_enabled.append(user_info.remove(user))
    print(len(pw_not_enabled))
    print(len(user_info))

    no_credentials = []
    for user in user_info:
        if (not "access_key_1_active" in user and
            not "access_key_2_active" in user and
            not user["password_enabled"] == 'true'
        ):
            no_credentials.append(user_info.remove(user))
    print(len(no_credentials))
    print(len(user_info))

    no_credentials += pw_not_enabled
    print(len(no_credentials))
    print(len(user_info))

    '''
    pw_never_used = [user for user in user_info
        if not "password_last_used" in user
        and is_more_than(90, user[""])
        and
    ]


    no_access_keys = [user for user in user_info if not "access_key_1_active" in user
            and not "access_key_2_active" in user]
    never_used = [user["Arn"] for user in pw_never_used if user in no_access_keys]

    key = "User never logged in"
    print(yamlfmt({key: never_used}))

    print(yamlfmt(pw_never_used))
        

    if days_since is not None:
        pw_last_used_more_than = [user for user in user_info
            if "password_last_used" in user
            and is_more_than(days_since, user["password_last_used"])
        ]

        accesskey1_last_used_less_than = [user for user in user_info
            if "access_key_1_last_used_date" in user
            and is_less_than(days_since, user["access_key_1_last_used_date"])
        ]
        accesskey2_last_used_less_than = [user for user in user_info
            if "access_key_2_last_used_date" in user
            and is_less_than(days_since, user["access_key_2_last_used_date"])
        ]
        accesskey_last_used_less_than = accesskey1_last_used_less_than + accesskey2_last_used_less_than

        user_last_used_more_than = [user["Arn"] for user in pw_last_used_more_than if user not in accesskey_last_used_less_than]
        key = "No access for over {} days".format(days_since)
        print(yamlfmt({key: user_last_used_more_than}))

        #print(len(pw_last_used_more_than))
        #print(yamlfmt(pw_last_used_more_than))

        #print(len(accesskey1_last_used_less_than))
        #print(yamlfmt(accesskey1_last_used_less_than))

        #print(len(accesskey2_last_used_less_than))
        #print(yamlfmt(accesskey2_last_used_less_than))

        #print(len(accesskey_last_used_less_than))
        #print(yamlfmt(accesskey_last_used_less_than))

        #print(len(user_last_used_more_than))
        #print(yamlfmt(user_last_used_more_than))

    '''


if __name__ == "__main__":
    main()
