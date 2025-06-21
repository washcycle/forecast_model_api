terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.37.1"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"
  # Remeber to check kubeconfig context so you don't accidentally deploy to the wrong cluster  
}
