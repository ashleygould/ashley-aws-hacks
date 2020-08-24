#!/bin/bash

# query ec2 tags by name.  Default is show all tags

INSTANCE_ID=$(ec2-metadata -i| awk {'print $2}')
EC2TAGS=$(aws ec2 describe-tags --filter Name=resource-id,Values=${INSTANCE_ID})
#echo $EC2TAGS
#echo $EC2TAGS | jq -r

if [ $# -ge 1 ]; then
  key=$1
  echo $EC2TAGS | jq -r ".Tags[] | select(.Key == \"$key\") | .Value"
else
  echo $EC2TAGS | jq -r '.Tags[] | [.Key, .Value] | join(":")'
fi
