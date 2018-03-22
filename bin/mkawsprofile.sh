#!/bin/bash
#set -x

ROLE="awsauth/OrgAdmin"
REPORTDIR="$HOME/tmp/loginprofiles"
USER=$1
MODE=$2
EMAIL=$3

REPORT=$REPORTDIR/${USER}.txt
awsloginprofile $USER --${MODE} --role $ROLE 2>&1 > $REPORT
status=$?
if [ $status -ne 0 ]; then
    cat $REPORT
    exit $status
fi

if [ -n "$EMAIL" ]; then
  echo | mail -s 'login profile' -c agould@ucop.edu -a $REPORT $EMAIL
fi
