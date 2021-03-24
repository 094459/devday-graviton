import os.path
from aws_cdk.aws_s3_assets import Asset
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core
)
dirname = os.path.dirname(__file__)

## Use these ranges to reduce the exposure of ssh access when setting up ingress rules

##  "ap-northeast-1": ["18.179.48.128/27", "18.179.48.96/27"],
##  "ap-northeast-2": ["15.164.243.192/27", "15.164.243.32/27"],
##  "ap-south-1": ["13.232.67.128/27", "13.232.67.160/27"],
##  "ap-southeast-1": ["13.250.186.128/27", "13.250.186.160/27"],
##  "ap-southeast-2": ["13.236.82.128/27", "13.236.82.96/27"],
##  "ca-central-1": ["15.222.16.96/27", "15.222.43.0/27"],
##  "eu-central-1": ["18.184.138.224/27", "18.184.203.128/27"],
##  "eu-north-1": ["13.48.186.128/27", "13.48.186.160/27"],
##  "eu-west-1": ["34.245.205.0/27", "34.245.205.64/27"],
##  "eu-west-2": ["3.10.127.32/27", "3.10.201.64/27"],
##  "eu-west-3": ["15.188.210.32/27", "15.188.210.64/27"],
##  "sa-east-1": ["18.230.46.0/27", "18.230.46.32/27"],
##  "us-east-1": ["35.172.155.192/27", "35.172.155.96/27"],
##  "us-east-2": ["18.188.9.0/27", "18.188.9.32/27"],
##  "us-west-1": ["13.52.232.224/27", "18.144.158.0/27"],
##  "us-west-2": ["34.217.141.224/27", "34.218.119.32/27"]


class Cloud9Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc,  **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            cpu_type=ec2.AmazonLinuxCpuType.ARM_64,
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
        #loadgen.allow_ssh_access_from(ec2.Peer.any_ipv4())
        #loadgen.allow_ssh_access_from(ec2.Peer.ipv4('10.44.0.0/24'))
        #loadgen.instance.instance.add_property_override("KeyName", key_name)
        
        c9SecurityGroup = ec2.SecurityGroup(
            self,
            'Cloud9 SecurityGroup',
            vpc=vpc,
            security_group_name="cloud9-ssh-access-sg",
            description= 'Allow ssh access to ec2 instances from anywhere',
            allow_all_outbound=True
        )
        
        c9SecurityGroup.add_ingress_rule(ec2.Peer.ipv4('18.184.138.224/27'), ec2.Port.tcp(22), 'allow c9 service ssh access')
        c9SecurityGroup.add_ingress_rule(ec2.Peer.ipv4('18.184.203.128/27'), ec2.Port.tcp(22), 'allow c9 service access')
        
        
        cloud9 = ec2.Instance(
            self,
            id="DemoCloud9IDE",
            vpc=vpc,
            instance_name="Cloud9",
            instance_type=ec2.InstanceType("m6g.large"),
            machine_image=amzn_linux,
            role = role,
            security_group = c9SecurityGroup
        )
        
        # We use session manager, but if you want to deploy an ssh key as above, you will need to open up ssh
        #mySecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), 'allow public ssh access')
        
        #asset = Asset(self, "Asset", path=os.path.join(dirname, "assets/load_deploy.sh"))
        asset = Asset(self, "Asset", path=os.path.join(dirname, "assets/userdata.sh"))
        local_path = cloud9.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key
        )
        
        cloud9.user_data.add_execute_file_command(file_path=local_path)
        asset.grant_read(cloud9.role)
            

        ec2.CfnEIP(self, id="C9HostEIP", domain="vpc", instance_id=cloud9.instance_id)
        
        core.CfnOutput(
            self,
            id="C9PrivateIP",
            value=cloud9.instance_private_ip,
            description="C9 Private IP",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:cloud9-private-ip"
        )

        core.CfnOutput(
            self,
            id="C9PublicIP",
            value=cloud9.instance_public_ip,
            description="C9 Public IP",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:cloud9-public-ip"
        )