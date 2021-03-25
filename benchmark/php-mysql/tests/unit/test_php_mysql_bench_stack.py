import json
import pytest

from aws_cdk import core
from php-mysql-bench.php_mysql_bench_stack import PhpMysqlBenchStack


def get_template():
    app = core.App()
    PhpMysqlBenchStack(app, "php-mysql-bench")
    return json.dumps(app.synth().get_stack("php-mysql-bench").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
