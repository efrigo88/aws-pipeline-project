locals {
  project_name = "ECS-pipeline"
  ecr_image    = "140023373701.dkr.ecr.eu-west-1.amazonaws.com/my-ecs-task-repo:latest"

  common_tags = {
    Project    = local.project_name
    Managed_By = "Terraform"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}