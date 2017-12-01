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

cfn-template() {
    aws cloudformation get-template --stack-name $1
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


# s3
s3ls() {
    bucket=$1
    if [ -n "$bucket" ]; then
        aws s3 ls s3://${bucket}/
    else
        aws s3 ls
    fi
}

s3sync() {
    bucket=$1
    target=$2
    if [ -n "$target" ]; then
        aws s3 sync s3://${bucket}/ $target/
    else
        aws s3 sync s3://${bucket}/ .
    fi
}


