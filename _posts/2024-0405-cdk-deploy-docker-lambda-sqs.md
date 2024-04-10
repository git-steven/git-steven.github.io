---
title:  "Feature Selection with scikit-learn"
date:   2024-03-29 13:18:25 -0500
categories:
- python
- lambda
- aws
- cdk
- SQS
- messaging
- message_queue
author: steven
---

# Deploying a Dockerized Python Lambda Function with AWS CDK

In this tutorial, we'll take a a look at the steps to deploy a dockerized Python Lambda function using AWS CDK (Cloud Development Kit). The Lambda function will be triggered by an SQS (Simple Queue Service) message.

## Prerequisites

Before we begin, make sure you have the following:

- AWS account with appropriate permissions
- AWS CLI installed and configured
- Node.js and npm installed
- AWS CDK installed (`npm install -g aws-cdk`)
- Docker installed

## Step 1: Create a new CDK project

First, create a new directory for your CDK project and initialize it:

```bash
mkdir my-lambda-project
cd my-lambda-project
cdk init app --language python
```

## Step 2: Install required dependencies

Install the necessary CDK dependencies for Lambda and SQS:

```bash
pip install aws-cdk-lib
```

## Step 3: Define the Lambda function

Create a new directory for your Lambda function and add your Python code:

```bash
mkdir lambda
touch lambda/app.py
```

Inside `lambda/app.py`, add your Lambda function code. For example:

```python
import json

def handler(event, context):
    message = json.loads(event['Records'][0]['body'])
    print(f"Received message: {message}")
    # Add your function logic here
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully')
    }
```

## Step 4: Create a Dockerfile

Create a `Dockerfile` in the `lambda` directory to package your Lambda function as a Docker container:

```dockerfile
FROM public.ecr.aws/lambda/python:3.8

COPY app.py /var/task/
CMD ["app.handler"]
```

## Step 5: Update the CDK stack

Open the `my_lambda_project_stack.py` file in your CDK project and update it with the following code:

```python
from aws_cdk import (
    aws_lambda as _lambda,
    aws_sqs as sqs,
    aws_lambda_event_sources as lambda_event_sources,
    Stack
)
from constructs import Construct

class MyLambdaProjectStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an SQS queue
        queue = sqs.Queue(self, "MyQueue")

        # Create a Lambda function from the Docker image
        function = _lambda.DockerImageFunction(
            self, "MyLambdaFunction",
            code=_lambda.DockerImageCode.from_image_asset("lambda")
        )

        # Add SQS event source to the Lambda function
        function.add_event_source(lambda_event_sources.SqsEventSource(queue))
```

## Step 6: Deploy the stack

Deploy the CDK stack to create the resources in your AWS account:

```bash
cdk deploy
```

Review the changes and confirm the deployment.

## Step 7: Test the Lambda function

Send a message to the SQS queue to trigger the Lambda function. You can use the AWS Management Console or the AWS CLI to send a message to the queue.

For example, using the AWS CLI:

```bash
aws sqs send-message --queue-url <queue-url> --message-body '{"key": "value"}'
```

Replace `<queue-url>` with the URL of your SQS queue.

Check the CloudWatch Logs for your Lambda function to verify that it was triggered and processed the message successfully.

That's it! You have successfully deployed a dockerized Python Lambda function using AWS CDK, triggered by an SQS message.

Remember to clean up the resources created in this tutorial by running `cdk destroy` when you're done to avoid incurring unnecessary costs.
