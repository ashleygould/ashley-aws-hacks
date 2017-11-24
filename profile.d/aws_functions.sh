#!/bin/bash

# cloudformation
cfn-delete() {
   aws cloudformation delete-stack --stack-name $1
}

cfn-events() {
    aws cloudformation describe-stack-events --stack-name $1 | less
}

cfn-list() {
    aws cloudformation describe-stacks | grep StackName
}

cfn-stack() {
    aws cloudformation describe-stacks --stack-name $1
}

# codecommit
ccom-list() {
    aws codecommit list-repositories
}

ccom-create() {
    aws codecommit create-repository --repository-name $1
}

ccom-delete() {
    aws codecommit delete-repository --repository-name $1
}

ccom-clone() {
    repo=$(cc-geturl.py $1)
    git clone $repo
}
    

# aws shell mfa stuff.
# this should go into aws-shelltools
EXPORT=$HOME/.aws/config.d/exported_env
aws-export() {
    env | grep --color=auto ^AWS | sort > $EXPORT
    perl -pi -e "s/^(.*)$/export \1/g" $EXPORT
    chmod 600 $EXPORT
}

aws-import() {
   list=$(grep -v EXPIRATION $EXPORT)
   echo $list
   eval $list

