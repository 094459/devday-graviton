#!/bin/bash

export BUCKET_NAME1=graviton-image-builder-demo-ricsue-arm
export BUCKET_NAME2=graviton-image-builder-demo-ricsue-x86
export STACK_NAME1=demo-graviton-ami-arm
export STACK_NAME1=demo-graviton-ami-x86
export SUBNETS=$( \
  echo $( \
    aws ec2 describe-subnets \
      --output text \
      --query 'Subnets[?DefaultForAz==`true`].SubnetId' \
  ) | sed "s/ /\\\,/g")

echo $SUBNETS
echo $BUCKET_NAME1
echo $BUCKET_NAME2
echo $STACK_NAME1
echo $STACK_NAME2

export STACK_ID1=$(
  aws cloudformation create-stack \
    --stack-name $STACK_NAME1 \
    --template-body file://cf-pipeline.yaml \
    --parameters \
    ParameterKey=InitialCodeBucketName,ParameterValue=$BUCKET_NAME1 \
    ParameterKey=Subnets,ParameterValue=$SUBNETS \
    ParameterKey=Architecture=arm64 \
    ParameterKey=InstanceType,ParameterValue=t4g.micro \
    --capabilities CAPABILITY_IAM \
    --output text \
    --query StackId)
    
export STACK_ID2=$(
  aws cloudformation update-stack \
    --stack-name $STACK_NAME2 \
    --template-body file://cf-pipeline.yaml \
    --parameters \
    ParameterKey=InitialCodeBucketName,ParameterValue=$BUCKET_NAME2 \
    ParameterKey=Subnets,ParameterValue=$SUBNETS \
    ParameterKey=Architecture,ParameterValue=arm64 \
    ParameterKey=InstanceType,ParameterValue=t4g.micro \
    --capabilities CAPABILITY_IAM \
    --output text \
    --query StackId)