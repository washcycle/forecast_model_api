variable "github_username" {
  description = "GitHub username for registry"
  type        = string
}

variable "github_token" {
  description = "GitHub token for registry"
  type        = string
  sensitive   = true
}