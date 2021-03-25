from aws_cdk import (
    core,
)

from Base import Base
from Pipeline import Pipeline

#this doesnt work yet, need to fix!
env_EU=core.Environment(region="eu-central-1")
props = {'namespace': 'graviton-multi-arch-pipeline','env':'env_EU'}
app = core.App()

# stack for ecr, bucket, codebuild
base = Base(app, f"{props['namespace']}-base", props)

# pipeline stack
pipeline = Pipeline(app, f"{props['namespace']}-pipeline", base.outputs)
pipeline.add_dependency(base)

app.synth()
