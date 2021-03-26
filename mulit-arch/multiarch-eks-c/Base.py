from aws_cdk import (
    aws_s3 as aws_s3,
    aws_ecr,
    aws_codebuild,
    aws_ssm,
    core,
)

class Base(core.Stack):
    def __init__(self, app: core.App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # pipeline requires versioned bucket
        bucket = aws_s3.Bucket(
            self, "SourceBucket",
            bucket_name=f"{props['namespace'].lower()}-{core.Aws.ACCOUNT_ID}",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY)
        # ssm parameter to get bucket name later
        bucket_param = aws_ssm.StringParameter(
            self, "ParameterB",
            parameter_name=f"{props['namespace']}-bucket",
            string_value=bucket.bucket_name,
            description='cdk pipeline bucket'
        )
        # ecr repo to push docker container into
        ecr = aws_ecr.Repository(
            self, "ECR",
            repository_name=f"{props['namespace']}",
            removal_policy=core.RemovalPolicy.DESTROY
        )
        # codebuild project meant to run in pipeline
        cb_docker_build = aws_codebuild.PipelineProject(
            self, "DockerBuild",
            project_name=f"{props['namespace']}-Docker-Build",
            build_spec=aws_codebuild.BuildSpec.from_source_filename(
                filename='buildspec.yml'),
            environment=aws_codebuild.BuildEnvironment(
                privileged=True,
                build_image=aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_3
            ),
            # pass the ecr repo uri into the codebuild project so codebuild knows where to push
            environment_variables={
                'ecr': aws_codebuild.BuildEnvironmentVariable(
                    value=ecr.repository_uri),
                'tag': aws_codebuild.BuildEnvironmentVariable(
                    value='cdk'),
                'AWS_DEFAULT_REGION': aws_codebuild.BuildEnvironmentVariable(
                    value='eu-west-1'),
                'AWS_ACCOUNT_ID': aws_codebuild.BuildEnvironmentVariable(
                    value='704533066374'),
                'IMAGE_REPO_NAME': aws_codebuild.BuildEnvironmentVariable(
                    value='demo-graviton-multi-arch'),
                'IMAGE_TAG': aws_codebuild.BuildEnvironmentVariable(
                    value='latest-amd64')
            },
            description='Pipeline for CodeBuild',
            timeout=core.Duration.minutes(60),
        )

        # codebuild for arm

        cb_docker_build_arm = aws_codebuild.PipelineProject(
            self, "DockerBuildArm",
            project_name=f"{props['namespace']}-Docker-Build-Arm",
            build_spec=aws_codebuild.BuildSpec.from_source_filename(
                filename='buildspec.yml'),
            environment=aws_codebuild.BuildEnvironment(
                privileged=True,
                build_image=aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_ARM
            ),
            # pass the ecr repo uri into the codebuild project so codebuild knows where to push
            environment_variables={
                'ecr': aws_codebuild.BuildEnvironmentVariable(
                    value=ecr.repository_uri),
                'tag': aws_codebuild.BuildEnvironmentVariable(
                    value='cdk'),
                'AWS_DEFAULT_REGION': aws_codebuild.BuildEnvironmentVariable(
                    value='eu-west-1'),
                'AWS_ACCOUNT_ID': aws_codebuild.BuildEnvironmentVariable(
                    value='704533066374'),
                'IMAGE_REPO_NAME': aws_codebuild.BuildEnvironmentVariable(
                    value='demo-graviton-multi-arch'),
                'IMAGE_TAG': aws_codebuild.BuildEnvironmentVariable(
                    value='latest-arm64v8')
            },
            description='Pipeline for CodeBuild',
            timeout=core.Duration.minutes(60),
        )        

        # codebuild for manifest

        cb_docker_build_manifest = aws_codebuild.PipelineProject(
            self, "DockerBuildManifest",
            project_name=f"{props['namespace']}-Docker-Build-Manifest",
            build_spec=aws_codebuild.BuildSpec.from_source_filename(
                filename='buildspec-manifest.yml'),
            environment=aws_codebuild.BuildEnvironment(
                privileged=True,
                #compute_type=SMALL|MEDIUM|LARGE,
                build_image=aws_codebuild.LinuxBuildImage.from_code_build_image_id("aws/codebuild/amazonlinux2-x86_64-standard:3.0")
                #build_image=aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_3
                #build_image=aws_codebuild.LinuxBuildImage.STANDARD_5_0 - use this if you want Ubuntu
            ),
            # pass the ecr repo uri into the codebuild project so codebuild knows where to push
            environment_variables={
                'ecr': aws_codebuild.BuildEnvironmentVariable(
                    value=ecr.repository_uri),
                'tag': aws_codebuild.BuildEnvironmentVariable(
                    value='cdk'),
                'AWS_DEFAULT_REGION': aws_codebuild.BuildEnvironmentVariable(
                    value='eu-west-1'),
                'AWS_ACCOUNT_ID': aws_codebuild.BuildEnvironmentVariable(
                    value='704533066374'),
                'IMAGE_REPO_NAME': aws_codebuild.BuildEnvironmentVariable(
                    value='demo-graviton-multi-arch'),
                'IMAGE_TAG': aws_codebuild.BuildEnvironmentVariable(
                    value='latest')
            },
            description='Pipeline for CodeBuild',
            timeout=core.Duration.minutes(60),
        )

        # codebuild iam permissions to read write s3
        bucket.grant_read_write(cb_docker_build)
        bucket.grant_read_write(cb_docker_build_arm)
        bucket.grant_read_write(cb_docker_build_manifest)

        # codebuild permissions to interact with ecr
        ecr.grant_pull_push(cb_docker_build)
        ecr.grant_pull_push(cb_docker_build_arm)
        ecr.grant_pull_push(cb_docker_build_manifest)

        core.CfnOutput(
            self, "ECRURI",
            description="ECR URI",
            value=ecr.repository_uri,
        )
        core.CfnOutput(
            self, "S3Bucket",
            description="S3 Bucket",
            value=bucket.bucket_name
        )

        self.output_props = props.copy()
        self.output_props['bucket']= bucket
        self.output_props['cb_docker_build'] = cb_docker_build
        self.output_props['cb_docker_build_arm'] = cb_docker_build_arm
        self.output_props['cb_docker_build_manifest'] = cb_docker_build_manifest

    # pass objects to another stack
    @property
    def outputs(self):
        return self.output_props
