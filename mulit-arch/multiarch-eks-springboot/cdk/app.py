import os

from aws_cdk import core

from pipeline.pipeline_stack import PipelineStack
from backend.backend_stack import BackendStack

env = core.Environment(account="704533066374",
                       region="eu-west-1")

app = core.App()

backend = BackendStack(app, "demo-multi-arch-springb-backend", env=env)
pipeline = PipelineStack(app, "demo-multi-arch-springb-pipeline", eks=backend.eks, env=env)

app.synth()
