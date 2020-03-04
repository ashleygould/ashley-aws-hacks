#!/usr/bin/env python
'''

find users with obsolete credentials:

    - user has no password and no access keys

    - user is more than 30 days old but has never logged in

    - user has not logged in for over X number of days.  default: one year


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
DEFAULT_UNUSED_CREDENTIALS_DAYS = 365


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


def is_less_than(number_of_days, date_str):
    return datetime.now() - str2datetime(date_str) < timedelta(days=int(number_of_days))


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--days-since',
    required=False,
    default=DEFAULT_UNUSED_CREDENTIALS_DAYS,
    help='Report users whose last access was more than X number of days ago.'
)
@click.option('--verbose',
    is_flag=True,
    required=False,
    default=False,
    help='Show full credentials report when printing results'
)
def main(days_since, verbose):

    user_info = credentials_report()

    # user is brand new
    new_users = []
    for user in user_info:
        if is_less_than(NEW_USER_GRACE_PERIOD, user["user_creation_time"]):
            new_users.append(user)
    for user in new_users:
        user_info.remove(user)

    # user has no password and no access keys
    pw_not_enabled = []
    for user in user_info:
        if not "password_enabled" in user:
            pw_not_enabled.append(user)
    for user in pw_not_enabled:
        user_info.remove(user)

    no_credentials = []
    for user in user_info:
        if (not "access_key_1_active" in user and
            not "access_key_2_active" in user and
            not user["password_enabled"] == 'true'
        ):
            no_credentials.append(user)
    for user in no_credentials:
        user_info.remove(user)

    no_credentials += pw_not_enabled


    # user has logged into the console in the last days_since days
    pw_used_within_limit = []
    for user in user_info:
        if "password_last_used" in user and is_less_than(days_since, user["password_last_used"]):
            pw_used_within_limit.append(user)
    for user in pw_used_within_limit:
        user_info.remove(user)


    # user has used access keys in the last days_since days
    accesskey1_used_within_limit = []
    for user in user_info:
        if "access_key_1_last_used_date" in user and is_less_than(days_since, user["access_key_1_last_used_date"]):
            accesskey1_used_within_limit.append(user)
    for user in accesskey1_used_within_limit:
        user_info.remove(user)

    accesskey2_used_within_limit = []
    for user in user_info:
        if "access_key_2_last_used_date" in user and is_less_than(days_since, user["access_key_2_last_used_date"]):
            accesskey2_used_within_limit.append(user)
    for user in accesskey2_used_within_limit:
        user_info.remove(user)


    # print results
    print("Users created in the last {} days:".format(NEW_USER_GRACE_PERIOD))
    if verbose:
        print(yamlfmt(new_users))
    else:
        print(yamlfmt([user["UserName"] for user in new_users]))

    print("Users have no credentials:")
    if verbose:
        print(yamlfmt(no_credentials))
    else:
        print(yamlfmt([user["UserName"] for user in no_credentials]))

    print("User access unused for over {} days".format(days_since))
    if verbose:
        print(yamlfmt(user_info))
    else:
        print(yamlfmt([user["UserName"] for user in user_info]))


if __name__ == "__main__":
    main()
