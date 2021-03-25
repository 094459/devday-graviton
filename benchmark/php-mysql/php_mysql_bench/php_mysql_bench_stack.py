import os.path
from aws_cdk.aws_s3_assets import Asset
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core
)

dirname = os.path.dirname(__file__)

class PhpMysqlBenchStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )
        
        # Allow to be managed via SSM
        
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))
        
        ## Setup key_name for EC2 instance login if you don't use Session Manager
        ## Create keypair in AWS console
        ## Change .any_ipv4 to a specific IP address/range to reduce attack surface

        #key_name = "{keypair}"
        #apachephp.allow_ssh_access_from(ec2.Peer.any_ipv4())
        #apachephp.allow_ssh_access_from(ec2.Peer.ipv4('10.44.0.0/24'))
        #apachephp.instance.instance.add_property_override("KeyName", key_name)
        
        mySecurityGroup = ec2.SecurityGroup(
            self,
            'ApachePHP SecurityGroup',
            vpc=vpc,
            security_group_name="apachephp-ssh-access-sg",
            description= 'Allow ssh and http/https access to ec2 instances from anywhere',
            allow_all_outbound=True
        )
        
        apachephp = ec2.Instance(
            self,
            id="LoadGen",
            vpc=vpc,
            vpc_subnets={"subnet_type": ec2.SubnetType.PUBLIC},
            instance_name="ApachePHP",
            instance_type=ec2.InstanceType("m5.xlarge"),
            machine_image=amzn_linux,
            role = role,
            security_group = mySecurityGroup
        )
        
        # lock down and change from any_ipv() to ipv4('CIDR') based on your network
        # do not leave this wide open as below.
        
        mySecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), 'allow public ssh access')
        mySecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), 'allow public http access')
        mySecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), 'allow public https access')
        
        asset = Asset(self, "Asset", path=os.path.join(dirname, "assets/http_deploy.sh"))
        local_path = apachephp.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key
        )
        
        apachephp.user_data.add_execute_file_command(file_path=local_path)
        asset.grant_read(apachephp.role)

            


        ec2.CfnEIP(self, id="ApachePHPHostEIP", domain="vpc", instance_id=apachephp.instance_id)
        
        core.CfnOutput(
            self,
            id="ApachePHPPrivateIP",
            value=apachephp.instance_private_ip,
            description="APACHE PHP Private IP",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:apachephp-private-ip"
        )

        core.CfnOutput(
            self,
            id="ApachePHPPublicIP",
            value=apachephp.instance_public_ip,
            description="APACHEPHP Public IP",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:apachephp-public-ip"
        )
        
