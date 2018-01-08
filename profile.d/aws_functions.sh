#!/bin/bash

aws-region() {
    export AWS_DEFAULT_REGION=$1
}



# iam

iam-listusers() {
    aws iam list-users | grep UserName
}

iam-listgroups() {
    aws iam list-groups | grep GroupName
}

iam-getuser() {
    aws iam get-user --user-name $1
    aws iam list-groups-for-user --user-name $1 | grep GroupName
}

iam-getgroup() {
    aws iam get-group --group-name $1 | grep -A 5 '"Group": {'
    aws iam get-group --group-name $1 | grep UserName
}

iam-useradd() {
    aws iam create-user --user-name $1
}

iam-userdel() {
    aws iam delete-user --user-name $1
}

iam-groupadd() {
    aws iam create-group --group-name $1
}

iam-groupdel() {
    aws iam delete-group --group-name $1
}

iam-groupmod-adduser() {
    aws iam add-user-to-group --group-name $1 --user-name $2
}

iam-groupmod-rmuser() {
    aws iam remove-user-from-group --group-name $1 --user-name $2
}




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
    aws cloudformation describe-stack-resources --stack-name $1
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

s3mb() {
    aws s3 mb s3://$1
}

s3rb() {
    aws s3 rb s3://$1
}

s3rrb() {
    aws s3 rm s3://$1 --recursive
    aws s3 rb s3://$1
}

s3put() {
    object=$1
    bucket=$2
    aws s3 cp $object s3://${bucket}/${object}
}

s3get() {
    object=$1
    bucket=$2
    aws s3 cp s3://${bucket}/${object} $object
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




# ecr

ecr-repos() {
    region=$1
    if [ -n "$region" ]; then
        aws ecr describe-repositories --region $region
    else
        aws ecr describe-repositories
    fi
}

ecr-create-repo() {
    repo=$1
    region=$2
    if [ -n "$region" ]; then
        aws ecr create-repository --repository-name $repo --region $region
    else
        aws ecr create-repository --repository-name $repo
    fi
}

ecr-delete-repo() {
    repo=$1
    tag=$2
    region=$3
    if [ -n "$region" ]; then
        aws ecr batch-delete-image --repository-name $repo --region $region --image-ids imageTag=${tag}
    else
        aws ecr batch-delete-image --repository-name $repo --image-ids imageTag=${tag}
    fi

    if [ -n "$region" ]; then
        aws ecr delete-repository --repository-name $repo --region $region
    else
        aws ecr delete-repository --repository-name $repo
    fi
}

ecr-images() {
    repo=$1
    region=$2
    if [ -n "$region" ]; then
        aws ecr describe-images --repository-name $repo --region $region
    else
        aws ecr describe-images --repository-name $repo
    fi
}

ecr-login() {
     eval $(aws ecr get-login --no-include-email)
}

