# FastAPI: Deploying a Dockerized FastAPI App to Fargate with AWS CDK

In this tutorial, we'll build on the Fast API application we created in [Part 1](https://git-steven.github.io/fastapi/python/jwt/authentication/security/fast-api-with-jwt/) of our FastAPI series.

We'll walk through the steps to deploy a dockerized Python FastAPI app using AWS CDK (Cloud Development Kit). We'll use AWS Fargate to run the dockerized FastAPI app as a serverless container.

Next we'll take a a look at the steps to deploy a dockerized Python Lambda function using AWS CDK (Cloud Development Kit). The Lambda function will be triggered by an SQS (Simple Queue Service) message.

We hinted at the end of the last tutorial that this is not a normal CRUD API.  We are following the [CQRS](https://martinfowler.com/bliki/CQRS.html) methodology; our writes will be physically separated from our reads and happen asynchronously.  The reads, however, will happen synchronously, right in our FastAPI application.

## Reads
Reads will occur synchronously in our FastAPI application.  They are implemented as one might expect.  The read logic (probably from the DB) is implemented and/or invoked from the appropriate endpoint.

## Writes
When an action occurs that requires changing state (e.g., writing to DB) are invoked via an asynchronous event.

### Production
Invocations to write in production will send an asynchronous SQS message.  That is picked up by a lambda function, that performs the the write based on the event type and the information in the message.

### Development
For simplicity (development, debugging, testing), there is no dependency on SQS.  Instead, we will [inject a dependency](https://en.wikipedia.org/wiki/Dependency_injection) to use a lightweight, no-dependency, intra-process, multithreaded, home-grown message queuing system called [Python Bunny MQ](https://github.com/tangledpath/python-bunny-mq)

![](https://raw.githubusercontent.com/tangledpath/python-bunny-mq/master/bunny-sm.png)

## Messaging system injection
Based on the value of `FAST_API_ENV`, we will inject either a façade that provides our message-queue functionality. Possible values and effects are:
    * development: Inject PythonBunnyMQ façade (for dev env)
* test: Inject PythonBunnyMQ façade (for test env)
* production: Inject AWS SQS MQ façade

## Prerequisites

Before we begin, make sure you have the following:

- AWS account with appropriate permissions
- AWS CLI installed and configured
- Node.js and npm installed
- AWS CDK installed (`npm install -g aws-cdk`)
- Docker installed

## Step 1: Install [python-bunny-mq](https://github.com/tangledpath/python-bunny-mq)

```bash
poetry add python-bunny-mq --group dev
```

## Step 2: Install [boto3](https://boto3.amazonaws.com/)
Boto3 allows us to interactive with Amazon services from Python.  Very cool!
```bash
poetry add boto3
```

## Step 1: Create a new CDK project

First, go to the root of the application (for example if you store your application repository in source.)
```bash
cd ~/src/

```bash
mkdir fastapi-cdk-project
cd fastapi-cdk-project
cdk init app --language python
```

## Step 2: Install required dependencies

Install the necessary CDK dependencies for ECS and ECR:

```bash
pip install aws-cdk-lib
```

## Step 3: Create the FastAPI app

Create a new directory for your FastAPI app and add the necessary files:

```bash
mkdir app
touch app/main.py app/Dockerfile app/requirements.txt
```

Inside `app/main.py`, add your FastAPI app code. For example:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

Inside `app/requirements.txt`, add the required Python dependencies:

```
fastapi
uvicorn
```

Inside `app/Dockerfile`, add the following:

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

## Step 4: Update the CDK stack

Open the `fastapi_cdk_project_stack.py` file in your CDK project and update it with the following code:

```python
from aws_cdk import (
    aws_ecs as ecs,
    aws_ecr_assets as ecr_assets,
    aws_ecs_patterns as ecs_patterns,
    Stack
)
from constructs import Construct

class FastapiCdkProjectStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an ECR asset from the Dockerfile
        docker_image = ecr_assets.DockerImageAsset(self, "FastAPIImage",
            directory="app"
        )

        # Create a Fargate service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "FastAPIService",
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_docker_image_asset(docker_image),
                container_port=80
            ),
            public_load_balancer=True
        )
```

## Step 5: Deploy the stack

Deploy the CDK stack to create the resources in your AWS account:

```bash
cdk deploy
```

Review the changes and confirm the deployment.

## Step 6: Access the FastAPI app

Once the deployment is complete, CDK will output the URL of the Application Load Balancer. Open that URL in your web browser to access your FastAPI app.

You should see the response `{"Hello": "World"}` from your FastAPI app.

That's it! You have successfully deployed a dockerized Python FastAPI app using AWS CDK and Fargate.

Remember to clean up the resources created in this tutorial by running `cdk destroy` when you're done to avoid incurring unnecessary costs.
