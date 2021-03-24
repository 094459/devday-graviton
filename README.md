## Getting start with AWS Graviton

Instructions on how to get these demos up and running on your AWS environment.

### 1. Setting up an AWS Cloud9 Development box

At the time of writing, you could not select AWS Graviton instance types when creating AWS Cloud9 development environments.

Until this changes, you can use this cdk app to provision an EC2 instance and then follow these instructions to create an ssh Cloud9 development environment.

Things to be aware of:

* The developer environment will not automatically hibernate, so make sure you stop/start the instances so you are not incurring costs when you are not using the environment
* Some of the integration that is done for you automatically when you spin up a Cloud 9 environment will need to be manually setup by yourself (for example, your AWS credentials)

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
cdk deploy c9-vpc
```

When that has completed, install the second stack, again answering y to any prompts.

```
cdk deploy c9-ide
```

Once this has completed, your environment is now setup. You can confirm this by going to the AWS console and checking the EC2 instances for the region you configured. You will need to connect to this instance in the next stage.

**Configuration**

