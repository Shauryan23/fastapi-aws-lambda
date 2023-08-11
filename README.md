# FastAPI Implementation Using AWS Lambda

**A Guide to Deploying Machine Learning Models Using AWS Lambda Function from Container Images**

---

Welcome to the **FastAPI using AWS Lambda** project! This project showcases the integration of _FastAPI_, a web framework for building APIs with Python, with _AWS Lambda_ using **containerization** of our app.

## Project's Goal

To demonstrate how to integrate and deploy a machine learning model as an api within a Docker container, utilizing the capabilities of AWS Lambda and Amazon ECR for container image deployment.

> In this project,
>
> - I've built an API using FastAPI _[app.py]_ which uses a machine learning model for classification using the model's pickle file.
> - Then I've encapsulated this API within a Docker container and deployed the container using Amazon Elastic Container Registry(ECR) .
> - Then create a Lambda function from the container image and adding Amazon API Gateway as a trigger.

Follow this **step-by-step guide** to:

- Set up the environment
- Build the Docker container image
- Deploy it to **AWS ECR**
- Create an **AWS Lambda** function
- Link it to an **API Gateway** trigger

## Prerequisites

- Python _(>3.8)_
- AWS account
- Docker
