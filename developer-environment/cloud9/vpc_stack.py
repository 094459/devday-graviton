from aws_cdk import (
    aws_ec2 as ec2,
    core
)

class VpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            id="DemoCloud9VPC",
            cidr="10.44.0.0/16",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", cidr_mask=24,
                    reserved=False, subnet_type=ec2.SubnetType.PUBLIC)
            ],
            enable_dns_hostnames=True,
            enable_dns_support=True
        )

