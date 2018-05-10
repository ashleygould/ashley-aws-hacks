#!/bin/bash
#set -x

usage() {
  echo "usage: $(basename $0) <username> <mode> <user-email>"
  echo "where 'mode' can be either 'new' or 'reset'"
}

if [ $# -ne 3 ]; then
  usage
  exit 1
fi

USER=$1
MODE=$2
EMAIL=$3

ROLE="awsauth/OrgAdmin"
CCEMAIL="agould@ucop.edu"
REPORTDIR="$HOME/tmp/loginprofiles"
REPORT=$REPORTDIR/${USER}.txt

awsloginprofile $USER --${MODE} --org-access-role $ROLE 2>&1 | tee $REPORT
status=$?
if [ $status -ne 0 ]; then
    cat $REPORT
    exit $status
fi

if [ -n "$EMAIL" ]; then
  echo | mail -s 'login profile' -c $CCEMAIL -a $REPORT $EMAIL
fi
