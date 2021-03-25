#!/usr/bin/env python3

from aws_cdk import core

from php_mysql_bench.vpc_stack import VpcStack
from php_mysql_bench.rds_mysql_stack import RDSMySQLStack
from php_mysql_bench.php_mysql_bench_stack import PhpMysqlBenchStack
from php_mysql_bench.loadgen_stack import LoadGenStack

#env_EU=core.Environment(region="eu-west-1")
env_EU=core.Environment(region="eu-central-1")

app = core.App()

#setup VPC network

vpc_stack = VpcStack(
    scope=app,
    id="vpc",
    env=env_EU
)

#setup RDS MySQL database

rds_stack = RDSMySQLStack(
    scope=app,
    id="rdsmysql",
    vpc=vpc_stack.vpc,
    env=env_EU
)

#setup LoadGen Box

load_stack = LoadGenStack(
    scope=app,
    id="loadgen",
    vpc=vpc_stack.vpc,
    env=env_EU
)

#setup PHP Box

php_stack = PhpMysqlBenchStack(
    scope=app,
    id="php-bench",
    vpc=vpc_stack.vpc,
    env=env_EU
)


app.synth()
