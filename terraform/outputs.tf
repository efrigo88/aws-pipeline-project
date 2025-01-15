output "ecs_cluster_name" {
  value = aws_ecs_cluster.ephemeral_cluster.name
}

output "ecs_task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

output "ecs_task_definition_arn" {
  value = aws_ecs_task_definition.ephemeral_task.arn
}

output "ecs_subnet_ids" {
  value = aws_subnet.ecs_subnet[*].id
}