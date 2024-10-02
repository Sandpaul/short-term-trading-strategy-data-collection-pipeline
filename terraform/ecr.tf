resource "aws_ecr_repository" "container_repo" {
  name = "short_term_trading_data_pipeline_ecr"
  image_tag_mutability = "MUTABLE"
}

output "repoistory_url" {
  value = aws_ecr_repository.container_repo.repository_url
}