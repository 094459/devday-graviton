## Getting start with AWS Graviton

Instructions on how to get these demos up and running on your AWS environment.

### 1. Setting up an AWS Cloud9 Development box

At the time of writing, you could not select AWS Graviton instance types when creating AWS Cloud9 development environments.

Until this changes, you can use this cdk app to provision an EC2 instance and then follow these instructions to create an ssh Cloud9 development environment.

Things to be aware of:

* The developer environment will not automatically hibernate, so make sure you stop/start the instances so you are not incurring costs when you are not using the environment
* Some of the integration that is done for you automatically when you spin up a Cloud 9 environment will need to be manually setup by yourself (for example, your AWS credentials)
* This does not configure an external facing EC2 instance, if you need to connect you can use Session Manager and connect as ec2-user

**Pre-Reqs**

- You will need to have a local developer environment that is setup and configured with the aws cli
- You will have installed cdk
- You are running a supported version of Python (>3.7) and the latest pip

**Installation**

Once you have checked out this repo into a local folder, go to the developer-environment folder and install the dependencies

```
$ cd <local source folder>
$ cd developer-environment
$ pip install -r requirements.txt
```

Make sure that the cdk app is ok by issuing the following command, which should output the two cdk stacks that you will create

```
$ cdk ls

c9-vpc
c9-ide
```

If you do not get that, then there is an issue which you will need to resolve before continuing.

You are now ready to deploy your AWS Graviton powered instance. Install the first stack, accepting y for any prompts.

```
$ cdk deploy c9-vpc
```

When that has completed, you should get some output like the following (with your own account details instead of these):

```
 ✅  c9-vpc

Outputs:
c9-vpc.ExportsOutputRefDemoCloud9VPC8871F024014B0437 = vpc-0b71bbf5af816ed31
c9-vpc.ExportsOutputRefDemoCloud9VPCpublicSubnet1Subnet7E5CFDAB950D0894 = subnet-0d9f74a4b2e34b953

Stack ARN:
arn:aws:cloudformation:eu-central-1:XXXXXXXXXX:stack/c9-vpc/9c7c3010-8750-11eb-ba3c-06ccf463d918
```

Install the second stack, again answering y to any prompts.

```
$ cdk deploy c9-ide
```

Once this has completed, your environment is now setup. You can confirm this by going to the AWS console and checking the EC2 instances for the region you configured. You will need to connect to this instance in the next stage.

**Configuration**

From the EC2 console, select the EC2 instance you have just created (the default is called Cloud9, but if you change it in the script it will be whatever you called it)

The first thing you are going to need to do is record the Public IPv4 DNS details for this instance, as we will be using that when we create the Cloud9 ssh environment.

The next thing you need to do is open up a ssh session to this instance. Given we have restricted access, us the Connect > Session Manager to connect. This will connect you as the ssm-user, so we will switch to the user we need

```
$ sudo su - ec2-user
```

Now we need to add the ssh public key into the .ssh/authorized_keys for the Cloud9 environment we are about to create. So lets get ready by going into that directory first

```
$ cd ~/.ssh
```

Now keep this tab open and open a new one (or navigate back) to the AWS Console, and go to the AWS Cloud9 console, using the same region that you created the EC2 instance in.

* Click on CREATE ENVIRONMENT and provide it a name (I am going to use, GravitonC9Demo) and click on NEXT STEPS.
* Select the THIRD option - Create and run in remote server (SSH connection)
* - For "User" enter ec2-user
* - For "Host" enter the Public IPv4 DNS details you saved above (it will be in the format of ec2-{ip}.{region}.compute.amazonaws.com)
* Click on COPY PUBLIC KEY

Now switch to the Session Manager tab, and you will now add this key to the authorized_keys file. 

```
$ echo {paste public key} >  authorized_keys
```
You can check the file to make sure the key has been added.

Now return back to the AWS Cloud9 create screen and click on NEXT STEP. If all is well you will see a REVIEW page, which you can now complete by clicking on CREATE ENVIRONMENT.

If everything has worked, the next screen you see should be the AWS Cloud9 introduction screen. From the terminal, enter the following command to validate that you are running on an AWS Graviton2 powered instance.

```
$ uname -m

aarch64
```
### 2. Benchmarking



### 3. Supporting multi architecture workloads



