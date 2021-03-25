from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    core
)

class RDSMySQLStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_21)
        
        db = rds.DatabaseInstance(self, "RDS",
            engine=engine,
            credentials=rds.Credentials.from_generated_secret("dbadmin"),
            vpc=vpc,
            vpc_placement=ec2.SubnetSelection(subnet_group_name="private"),
            port=3306,
            storage_encrypted=True,
            instance_type= ec2.InstanceType("m6g.4xlarge"),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            publicly_accessible=False,
            database_name="gravitondemodb"
        )
        
        db.connections.allow_default_port_from(ec2.Peer.ipv4('10.0.0.0/16'))
