import os.path
from aws_cdk.aws_s3_assets import Asset
from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core
)

dirname = os.path.dirname(__file__)


class LoadGenStack(core.Stack):

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
        #loadgen.allow_ssh_access_from(ec2.Peer.any_ipv4())
        #loadgen.allow_ssh_access_from(ec2.Peer.ipv4('10.44.0.0/24'))
        #loadgen.instance.instance.add_property_override("KeyName", key_name)
        
        mySecurityGroup = ec2.SecurityGroup(
            self,
            'Loadgen SecurityGroup',
            vpc=vpc,
            security_group_name="loadgen-ssh-access-sg",
            description= 'Allow ssh access to ec2 instances from anywhere',
            allow_all_outbound=True
        )
        
        loadgen = ec2.Instance(
            self,
            id="LoadGen",
            vpc=vpc,
            instance_name="LoadGen",
            instance_type=ec2.InstanceType("m5.xlarge"),
            machine_image=amzn_linux,
            role = role,
            security_group = mySecurityGroup
        )
        
        # We use session manager, but if you want to deploy an ssh key as above, you will need to open up ssh
        #mySecurityGroup.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), 'allow public ssh access')
        
        asset = Asset(self, "Asset", path=os.path.join(dirname, "assets/load_deploy.sh"))
        local_path = loadgen.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key
        )
        
        loadgen.user_data.add_execute_file_command(file_path=local_path)
        asset.grant_read(loadgen.role)
            

        ec2.CfnEIP(self, id="LoadGenHostEIP", domain="vpc", instance_id=loadgen.instance_id)
        
        core.CfnOutput(
            self,
            id="LoadGenPrivateIP",
            value=loadgen.instance_private_ip,
            description="LOADGEN Private IP",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:loadgen-private-ip"
        )

        core.CfnOutput(
            self,
            id="LoadgenPublicIP",
            value=loadgen.instance_public_ip,
            description="LOADGEN Public IP",
            export_name=f"{self.region}:{self.account}:{self.stack_name}:loadgen-public-ip"
        )
        
