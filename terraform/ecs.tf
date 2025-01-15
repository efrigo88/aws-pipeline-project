resource "aws_ecs_cluster" "ephemeral_cluster" {
  name = "ephemeral-cluster"

  tags = local.common_tags
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole"

  assume_role_policy = jsonencode({
    Version : "2012-10-17",
    Statement : [
      {
        Effect : "Allow",
        Principal : {
          Service : "ecs-tasks.amazonaws.com"
        },
        Action : "sts:AssumeRole"
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_ecs_task_definition" "ephemeral_task" {
  family                   = "ephemeral-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "ephemeral-container"
      image     = local.ecr_image
      essential = true
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_logs.name
          awslogs-region        = "eu-west-1"
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
  tags = local.common_tags
}

resource "aws_ecs_service" "ephemeral_service" {
  name            = "ephemeral-service"
  cluster         = aws_ecs_cluster.ephemeral_cluster.id
  launch_type     = "FARGATE"
  desired_count   = 1
  task_definition = aws_ecs_task_definition.ephemeral_task.arn

  network_configuration {
    subnets          = aws_subnet.ecs_subnet[*].id
    security_groups  = [aws_security_group.ecs_security_group.id]
    assign_public_ip = true
  }

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_cloudwatch_log_group" "ecs_task_logs" {
  name              = "/ecs/ephemeral-cluster"
  retention_in_days = 7

  tags = local.common_tags
}