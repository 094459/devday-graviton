from aws_cdk import (
    aws_codepipeline,
    aws_codepipeline_actions,
    aws_codecommit as codecommit,
    aws_ssm,
    core,
)

class Pipeline(core.Stack):
    def __init__(self, app: core.App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)
        # define the s3 artifact
        source_output = aws_codepipeline.Artifact(artifact_name='source')
        # define the pipeline
        pipeline = aws_codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name=f"{props['namespace']}",
            artifact_bucket=props['bucket'],
            stages=[
                aws_codepipeline.StageProps(
                    stage_name='Source',
                    actions=[
                        aws_codepipeline_actions.CodeCommitSourceAction(
                            # use this to create a new repo
                            # repository=codecommit.Repository(self, "multi-arch-hello-graviton-c", repository_name="multi-arch-hello-graviton-c"),
                            # use this to connect to an existing repo
                            repository=codecommit.Repository.from_repository_name(self, "hello-graviton-c","hello-graviton-c"),
                            action_name='CodeCommitSource',
                            run_order=1,
                            branch='main',
                            output=source_output
                        ),
                    ]
                ),
                aws_codepipeline.StageProps(
                    stage_name='Build',
                    actions=[
                        aws_codepipeline_actions.CodeBuildAction(
                            action_name='DockerBuildImages',
                            input=source_output,
                            project=props['cb_docker_build'],
                            run_order=1,
                        )
                    ]
                ),
                aws_codepipeline.StageProps(
                    stage_name='BuildArm',
                    actions=[
                        aws_codepipeline_actions.CodeBuildAction(
                            action_name='DockerBuildImages',
                            input=source_output,
                            project=props['cb_docker_build_arm'],
                            run_order=1,
                        )
                    ]
                ),
                aws_codepipeline.StageProps(
                    stage_name='BuildManifest',
                    actions=[
                        aws_codepipeline_actions.CodeBuildAction(
                            action_name='DockerBuildImages',
                            input=source_output,
                            project=props['cb_docker_build_manifest'],
                            run_order=2,
                        )
                    ]
                )
            ]

        )
        # give pipelinerole read write to the bucket
        props['bucket'].grant_read_write(pipeline.role)

        #pipeline param to get the
        pipeline_param = aws_ssm.StringParameter(
            self, "PipelineParam",
            parameter_name=f"{props['namespace']}-pipeline",
            string_value=pipeline.pipeline_name,
            description='cdk pipeline bucket'
        )
        # cfn output
        core.CfnOutput(
            self, "PipelineOut",
            description="Pipeline",
            value=pipeline.pipeline_name
        )
