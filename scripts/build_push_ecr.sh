#!/bin/bash
# Build Docker image
docker build --platform=linux/amd64 -t my-ecs-task:latest -f ../api/Dockerfile ../api

# Create an ECR Repository
# aws ecr create-repository --repository-name my-ecs-task-repo

# Authenticate Docker to ECR
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 140023373701.dkr.ecr.eu-west-1.amazonaws.com

# Tag and push image to ECR
docker tag my-ecs-task:latest 140023373701.dkr.ecr.eu-west-1.amazonaws.com/my-ecs-task-repo:latest
docker push 140023373701.dkr.ecr.eu-west-1.amazonaws.com/my-ecs-task-repo:latest