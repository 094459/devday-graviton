#!/usr/bin/env python3

from aws_cdk import core as cdk
from aws_cdk import core

from cloud9.cloud9_stack import Cloud9Stack
from cloud9.vpc_stack import VpcStack

#change to your environment
env_EU=core.Environment(region="eu-central-1")
app = core.App()

#setup VPC network

vpc_stack = VpcStack(
    scope=app,
    id="c9-vpc",
    env=env_EU
)

#setup Cloud9 IDE

rds_stack = Cloud9Stack(
    scope=app,
    id="c9-ide",
    vpc=vpc_stack.vpc,
    env=env_EU
)

app.synth()
