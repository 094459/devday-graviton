## Getting start with AWS Graviton

Instructions on how to get these demos up and running on your AWS environment.

### 1. AWS Developer tools running on AWS Graviton2 powered instances

As part of this demo, you will get to see how the AWS developer tooling works happily across x86 and aarch64 environments. Whilst for some of these there is no direct/integrated approach to using AWS Graviton2 instances, in the fullness of time we can expect to see that happen.

**AWS Cloud9, AWS CLI, AWS CDK**

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

**Post installation**

Once you have access to this, there are a few things you are going to need to do:

1. Configure your aws credentials using the "aws configure" command, which will ensure you can use the aws cli to interact with AWS.
2. Install any additional tools you might want to use - remember that you will need to look for aarch64 versions of those tools, or compile them via source. The build should have the essential tools you need to do this already installed.
3. For some EKS demos later, you can install the kubectl and eksctl tools, both of which run happily on aarch64

```
$ cd
$ curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_arm64.tar.gz" | tar xz -C /tmp
$ sudo mv /tmp/eksctl /usr/local/bin
$ curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.12/2020-11-02/bin/linux/arm64/kubectl
$ chmod +x ./kubectl
$ mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
```

### 2. Workload choice

AWS Graviton2 instances provide customers with more choice to run their workloads. When thinking about which workloads might make good candidates, you will probably want to perform some kind of assessment and analysis of your own applications to see how they perform.

There are plenty of benchmarks that have been produced, but these should be used as a starting point only. There is no substitate for doing your own baseline testing, especially if you already have workloads that are integrated into performance tests as part of your CI/CD testing approach.

The aim of this phase is to make sure you have the data you need to make the right workload choices.

**Methodology**

You should leverage your own methodology when it comes to running these tests. As mentioned before, general benchmarks, even benchmarks done by other folk are good general indicators, but you really want to understand what this means for your particular workloads which means coming up with a method for using the tools, the elastic benchmark environment that you can easily spin up in AWS and your application to generate the data to determine the level of price/performance improvements you are likely to see.

Once you have your data, you then need to work out the price/performance. For the MySQL benchmark using sysbench it is a simple calculation, where I use the transactions/per second as my metric (with higher being better). Yours may differ.

* For benchmark data where higher numbers are better, take the source metric and divide it by the on demand cost for the instance type you used during that benchmark
* For benchmark data where lower numbers are better, take the source metric and multiply it by the on demand cost for the instance type used during the benchmark

This will give you the relative price/performance difference, so even if one of the actual source metrics performes about the same, once you have factored in the lower costs of AWS Graviton2 instance types, then you can present the difference.

Make sure you think about how you capture the system information during the benchmark process - you want to capture the system characteristics (cpu, io, memory, etc) so that you can compare how running the workloads changes. Depending on your results, you might iterate and dive deep here, using application profiling tools for example to create flame graphs to see where there are optimisations or bottlenecks as part of the tests

![example report](images/grav-bench.png)

**Tools**

There are plenty of open source tools to help you benchmark your tools. Here are just some of the ones I have used:

- JMeter - you can created quite sophisticated tests via the gui, and then run these headless via a number of loaddrivers
- Apache ab - a good general purpose and easy to get started load driver
- Sysbench - a good tool for load testing databases

Finally you should look to script and make reproducable your benchmarking work so you can reproduce the results, baseline them over time and keep on top of this.

I have provided within the benchmarking folder a cdk app that deploys a number of services that you can use that creates tools that you could use as a basis for benchmarking. A number of tools has been deployed and configured and are ready to go, to make it easy for you.

### 3. Supporting multi architecture workloads



