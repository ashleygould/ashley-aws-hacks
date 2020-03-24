#!/bin/bash

aws-region() {
    region=$1
    if [ -n "$region" ]; then
    	export AWS_DEFAULT_REGION=$1
    else
	echo $AWS_DEFAULT_REGION
    fi
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


# IAM roles
iam-lr() {
    aws iam list-roles | grep RoleName
}

iam-role() {
    aws iam get-role --role-name $1
    aws iam list-role-policies --role-name $1
}

iam-role-policy() {
    aws iam get-role-policy --role-name $1 --policy-name $2
}



# cloudformation
cfn-delete() {
   aws cloudformation delete-stack --stack-name $1
}

cfn-events() {
    aws cloudformation describe-stack-events --stack-name $1 | jq -r '.StackEvents[] | .LogicalResourceId, .PhysicalResourceId, .ResourceType, .Timestamp, .ResourceStatus, .ResourceStatusReason, .ResourceProperties, ""'
}

cfn-list() {
    aws cloudformation describe-stacks | jq -r '.Stacks[].StackName'
}

cfn-stack() {
    aws cloudformation describe-stacks --stack-name $1 | jq -r '.Stacks[]'
    aws cloudformation describe-stack-resources --stack-name $1 | jq -r '.StackResources[] | .LogicalResourceId, .ResourceType, .ResourceStatus, ""'
}

cfn-template() {
    aws cloudformation get-template --stack-name $1 --output json| jq -r  '.TemplateBody'
}

cfn-cancel() {
    aws cloudformation cancel-update-stack --stack-name $1
}

cfn-resources() {
    aws cloudformation describe-stack-resources --stack-name $1
}

cfn-drift() {
    aws cloudformation detect-stack-drift --stack-name $1
    sleep 10
    aws cloudformation describe-stack-resource-drifts --stack-name $1
}




# codecommit
coco-list() {
    aws codecommit list-repositories
}

coco-create() {
    aws codecommit create-repository --repository-name $1
}

coco-delete() {
    aws codecommit delete-repository --repository-name $1
}

coco-clone() {
    repo=$(coco-geturl.py $1)
    git clone $repo
}




# s3
#
s3ls() {
    bucket=$1
    if [ -n "$bucket" ]; then
        aws s3 ls s3://${bucket}/
    else
        aws s3 ls | awk '{print $3}'
    fi
}
# for bucket in $(s3ls); do s3show.py $bucket; echo;echo; done | tee /tmp/bucket_inventory

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

s3syncto() {
    source=$1
    bucket=$2
    aws s3 sync $source/ s3://${bucket}/
}

s3syncfrom() {
    bucket=$1
    target=$2
    aws s3 sync s3://${bucket}/ $target/
}

s3encryptbucket() {
    bucket=$1
    aws s3api put-bucket-encryption --bucket $bucket --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'
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

# docker tag 035819119057.dkr.ecr.us-west-2.amazonaws.com/ucop_simplesamlphp:latest 071826132890.dkr.ecr.us-west-2.amazonaws.com/simplesamlphp:latest
# docker push 071826132890.dkr.ecr.us-west-2.amazonaws.com/simplesamlphp:latest




# ACM
acm-list() {
    region=$1
    if [ -n "$region" ]; then
	aws acm list-certificates --region $region
    else
	aws acm list-certificates
    fi
}

acm-cert() {
    url=$1
    region=$2
    if [ -n "$region" ]; then
	export AWS_DEFAULT_REGION=$region
	certarn=$(acm-getarn.py $url)
        aws acm describe-certificate --certificate-arn $certarn --region $region
    else
    	certarn=$(acm-getarn.py $url)
        aws acm describe-certificate --certificate-arn $certarn
    fi
}

acm-delete() {
    url=$1
    region=$2
    if [ -n "$region" ]; then
	export AWS_DEFAULT_REGION=$region
	certarn=$(acm-getarn.py $url)
        aws acm delete-certificate --certificate-arn $certarn --region $region
    else
    	certarn=$(acm-getarn.py $url)
        aws acm delete-certificate --certificate-arn $certarn
    fi
}


# Route53
r53-list() {
    aws route53 list-hosted-zones
}

r53-delete() {
    aws route53 delete-hosted-zone --id $1
}


# EC2 key-pairs
ec2-key-import() {
    PRIVATE_KEYNAME=$1
    EC2_KEYNAME=$2
    aws ec2 import-key-pair --key-name $EC2_KEYNAME --public-key-material file://~/.ssh/$PRIVATE_KEYNAME.pub
}

ec2-key-list() {
    EC2_KEYNAME=$1
    [ -z "$EC2_KEYNAME" ] && EC2_KEYNAME=""
    aws ec2 describe-key-pairs --key-names $EC2_KEYNAME
}


ec2-key-delete() {
    EC2_KEYNAME=$1
    aws ec2 delete-key-pair --key-name $EC2_KEYNAME
}


# EC2 AMI
ami-list() {
    #aws ec2 describe-images --owners self --query 'Images[*].{Name:Name, Id:ImageId, Date:CreationDate}' 
    #aws ec2 describe-images --owners self --output json | jq -r '.Images | sort_by(.CreationDate) | .[] | {"Name": .Name, "ImageId": .ImageId}'
    aws ec2 describe-images --owners self --output json | jq -r '.Images | sort_by(.CreationDate) | .[] | .ImageId, .Name, ""'
}

ami-get-snapshot() {
    aws ec2 describe-images --owners self --image-id $1 --output json | jq -r '.Images[].BlockDeviceMappings[] | select(.Ebs != null ) | .Ebs.SnapshotId'
}

ami-delete() {
    snaps=$(ami-get-snapshot $1)
    aws ec2 deregister-image --image-id $1
    for id in $snaps; do
	if [ -n $id ]; then
	    aws ec2 delete-snapshot --snapshot-id $id
        fi
    done
}


# EC2 Instances
#

ec2-instance-list() {
    aws ec2 describe-instances | \
	jq -r '.Reservations[].Instances[] | (select(.Tags != null) | .Tags[] | select(.Key == "Name") | .Value), .InstanceId, .PrivateIpAddress, .PublicIpAddress, .State.Name, ""'
}

ec2-instance-list-notags() {
    aws ec2 describe-instances | jq -r '.Reservations[].Instances[] | select(.Tags == null) | .InstanceId, .KeyName, .State.Name, ""'
}

ec2-instance-list-byname() {
    NAME=$1
    aws ec2 describe-instances --filters "Name=tag:Name,Values=$NAME" | \
	jq -r '.Reservations[].Instances[] | .InstanceId, .PrivateIpAddress, .PublicIpAddress, .KeyName, .State.Name, ""'
}

ec2-instance-list-ipbyname() {
    NAME=$1
    aws ec2 describe-instances --filters "Name=tag:Name,Values=$NAME" | \
	jq -r '.Reservations[].Instances[].PublicIpAddress'
}

ec2-instance-list-bykey() {
    KEY=$1
    aws ec2 describe-instances --filters "Name=key-name,Values=$KEY" | \
	jq -r '.Reservations[].Instances[] | .InstanceId, .PrivateIpAddress, .PublicIpAddress, .State.Name, .Tags, ""'
}

ec2-instance-list-byid() {
    ID=$1
    aws ec2 describe-instances --instance-ids $ID | \
	jq -r '.Reservations[].Instances[] | .PrivateIpAddress, .PublicIpAddress, .State.Name, .KeyName, .Tags, ""'
}

ec2-instance-list-running() {
    aws ec2 describe-instances | \
        jq -r '.Reservations[].Instances[] | select(.State.Name == "running") | .InstanceId'
}

ec2-instance-list-stopped() {
    aws ec2 describe-instances | \
        jq -r '.Reservations[].Instances[] | select(.State.Name == "stopped") | .InstanceId, .StateTransitionReason, .Tags'
}


ec2-instance-setname() {
    ID=$1
    NAME=$2
    aws ec2 create-tags --resources $ID --tags Key=Name,Value=$NAME
}

ec2-instance-ssh() {
    NAME=$1
    KEY=$2
    IP=$(ec2-instance-ipbyname $NAME)
    ssh -i ~/.ssh/$KEY ec2-user@$IP
}

ec2-instance-terminate() {
    ID=$1
    aws ec2 terminate-instances --instance-ids $ID
}


# ec2 SecurityGoups

ec2-vpc-list() {
  #aws ec2 describe-vpcs | jq -r '.Vpcs[] | .VpcId, .CidrBlock, .Tags, ""'
  aws ec2 describe-vpcs | jq -r '.Vpcs[] | .VpcId, .CidrBlock, ""'
}

ec2-vpc-list-tags() {
  aws ec2 describe-vpcs | jq -r '.Vpcs[] | .VpcId, .CidrBlock, .Tags, ""'
}


ec2-subnet-list() {
  vpc_id=$1
  aws ec2 describe-subnets | jq -r ".Subnets[] | .SubnetId, .CidrBlock, .AvailabilityZone, .VpcId, \"\""
}

ec2-subnet-list-by-vpc() {
  vpc_id=$1
  aws ec2 describe-subnets | jq -r ".Subnets[] | select(.VpcId == \"$vpc_id\") | .SubnetId, .CidrBlock, .AvailabilityZone, .VpcId, \"\""
}

ec2-sg-list-by-vpc() {
  vpc_id=$1
  aws ec2 describe-security-groups | jq -r ".SecurityGroups[] | select(.VpcId == \"$vpc_id\") | .GroupName, .Description, .GroupId, .VpcId, \"\""
}

ec2-sg-list() {
aws ec2 describe-security-groups | jq -r '.SecurityGroups[] | .GroupName, .Description, .GroupId, .VpcId, ""'
}

ec2-sg-delete() {
  sg_id=$1
  aws ec2 delete-security-group --group-id $sg_id
}

ec2-sg-delete-by-vpc() {
  vpc_id=$1
  sg_list=$(aws ec2 describe-security-groups | jq -r ".SecurityGroups[] | select(.VpcId == \"$vpc_id\") | .GroupId")
  echo $sg_list
  for sg_id in $sg_list; do
    aws ec2 delete-security-group --group-id $sg_id
  done
}



ec2-eni-list() {
aws ec2 describe-network-interfaces | jq -r '.NetworkInterfaces[] | .InterfaceType, .Description, .NetworkInterfaceId, .VpcId, .SubnetId, .PrivateIpAddress, ""'
}

ec2-eni-list-by-sg() {
aws ec2 describe-network-interfaces --filters Name=group-id,Values=$1 | jq -r '.NetworkInterfaces[] | .NetworkInterfaceId'
#aws ec2 describe-network-interfaces --filters Name=group-id,Values=$1
}



# SSM

ssm-param-history() {
    aws ssm get-parameter-history --name $1
}


# aws ssm get-parameter --name /ucop-ami-builder/amazonlinux2 | jq -r '.Parameter.Version'
#  1021  aws ssm put-parameter --name /ucop-ami-builder/amazonlinux2/latest --value ami-053111654d3b48b13 --type String
#  1029  aws ssm put-parameter --name /ucop-ami-builder/amazonlinux2/latest --value ami-053111654d3b48b13 --type String --overwrite
#  1030  aws ssm get-parameter --name /ucop-ami-builder/amazonlinux2/latest
#  1031  aws ssm get-parameter-history --name /ucop-ami-builder/amazonlinux2/latest
#  1032  aws ssm delete-parameter  --name /ucop-ami-builder/amazonlinux2/latest
#  1034  aws ssm put-parameter --name /ucop-ami-builder/amazonlinux2 --value ami-053111654d3b48b13 --type String --overwrite
#  1035  aws ssm get-parameter --name /ucop-ami-builder/amazonlinux2
#  1037  aws ssm get-parameter --name /ucop-ami-builder/amazonlinux2 | jq -r '.Parameter.Version'
#  1039  aws ssm get-parameter-history --name /ucop-ami-builder/amazonlinux2
#  1040  aws ssm get-parameter-history --name /ucop-ami-builder/amazonlinux2 | jq -r '.Parameters[].Version'
#  1041  aws ssm get-parameter-history --name /ucop-ami-builder/amazonlinux2 | jq -r '.Parameters[]'
#  1048  aws ssm delete-parameter --name /ucop-ami-builder/amazonlinux2
#  1049  aws ssm describe-parameters 
#  1050  aws ssm put-parameter --name /ucop-ami-builder/amazonlinux2 --value ami-053111654d3b48b13 --type String --overwrite --description amzn2-ami-hvm-ucop-1555438467-x86_64-gp2
#  1055  aws ssm delete-parameter --name /ucop-ami-builder/amazonlinux2
#  1056  aws ssm put-parameter --name /ucop-ami-builder/amazonlinux2 --value ami-053111654d3b48b13 --type String --description amzn2-ami-hvm-ucop-1555438467-x86_64-gp2 --tags Key=Name,Value=amzn2-ami-hvm-ucop-1555438467-x86_64-gp2
#  1070  aws ssm put-parameter --name /ucop-ami-builder/amazonlinux2 --value ami-053111654d3b48b13 --type String --description amzn2-ami-hvm-ucop-1555438467-x86_64-gp2 --overwrite
#  1073  aws ssm label-parameter-version --name /ucop-ami-builder/amazonlinux2 --labels latest


# Lambda

lambda-list() {
    aws lambda list-functions | jq -r .Functions[].FunctionName
}

lambda-policy() {
    aws lambda get-policy --function-name $1 --output text | jq -r . 2>/dev/null
}

lambda-function() {
    aws lambda get-function-configuration --function-name $1
}

lambda-function-full() {
    aws lambda get-function --function-name $1
}

lambda-update() {
    bucket=$1
    key=$2
    name=$3
    aws lambda update-function-code --s3-bucket $bucket --s3-key $key --function-name $name
}


lambda-delete() {
    aws lambda delete-function --function-name $1
}




# Config

config-list() {
    aws configservice describe-config-rules | jq -r .ConfigRules[].ConfigRuleName
}

config-rule() {
    aws configservice describe-config-rules --config-rule-names $1 | jq -r .ConfigRules[]
}

config-tags() {
    arn=$(aws configservice describe-config-rules --config-rule-names $1 | jq -r .ConfigRules[].ConfigRuleArn)
    echo $arn
    aws configservice list-tags-for-resource --resource-arn $arn
}

config-delete() {
    aws configservice delete-config-rule --config-rule-name $1
}

config-run() {
    aws configservice start-config-rules-evaluation --config-rule-names $1
}	

config-result() {
    aws configservice describe-compliance-by-config-rule --config-rule-names $1 | jq -r '.ComplianceByConfigRules[] | .ConfigRuleName, .Compliance.ComplianceType'
}

config-noncompliant() {
    aws configservice describe-compliance-by-config-rule | jq -r '.ComplianceByConfigRules[] | select(.Compliance.ComplianceType == "NON_COMPLIANT") | .ConfigRuleName'
}

config-compliant() {
    aws configservice describe-compliance-by-config-rule | jq -r '.ComplianceByConfigRules[] | select(.Compliance.ComplianceType == "COMPLIANT") | .ConfigRuleName'
}

config-details() {
    aws configservice get-compliance-details-by-config-rule --config-rule-name $1
}

# config infra

config-status() {
    aws configservice get-status
}

config-dc() {
    aws configservice describe-delivery-channels
    aws configservice describe-delivery-channel-status
}

config-rec() {
    aws configservice describe-configuration-recorders
}


