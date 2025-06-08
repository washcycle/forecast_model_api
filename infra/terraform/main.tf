resource "kubernetes_namespace" "apis" {
  metadata {
    name = "apis"
  }
}


resource "kubernetes_secret" "github_registry" {
  metadata {
    name      = "github-registry-secret"
    namespace = kubernetes_namespace.apis.metadata[0].name
    annotations = {
      "kubernetes.io/created-by" = "terraform"
    }
  }

  data = {
    ".dockerconfigjson" = jsonencode({
      auths = {
        "ghcr.io" = {
          auth = base64encode("${var.github_username}:${var.github_token}")
        }
      }
    })
  }

  type = "kubernetes.io/dockerconfigjson"
}

resource "kubernetes_deployment" "model" {
  metadata {
    name      = "model-deployment"
    namespace = kubernetes_namespace.apis.metadata[0].name
    labels = {
      app = "model"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "model"
      }
    }

    template {
      metadata {
        labels = {
          app = "model"
        }
      }

      spec {
        image_pull_secrets {
          name = kubernetes_secret.github_registry.metadata[0].name
        }

        container {
          name  = "model"
          image = "ghcr.io/washcycle/forecast-model-api:latest"

          port {
            name           = "http"
            container_port = 8000
          }
        }
      }
    }
  }
}

resource "kubernetes_horizontal_pod_autoscaler_v2" "model_hpa" {
  metadata {
    name      = "model-hpa"
    namespace = kubernetes_namespace.apis.metadata[0].name
  }

  spec {
    scale_target_ref {
      kind        = "Deployment"
      name        = kubernetes_deployment.model.metadata[0].name
      api_version = "apps/v1"
    }

    min_replicas = 1
    max_replicas = 5

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = 50
        }
      }
    }
  }
}

resource "kubernetes_service" "model_service" {
  metadata {
    name      = "model-service"
    namespace = kubernetes_namespace.apis.metadata[0].name
  }

  spec {
    selector = {
      app = kubernetes_deployment.model.metadata[0].labels.app
    }

    port {
      name        = "http"
      port        = 80
      target_port = 8000
    }

    type = "ClusterIP"
  }
}

resource "kubernetes_ingress_v1" "model_ingress" {
  metadata {
    name      = "tailscale-model-ingress"
    namespace = kubernetes_namespace.apis.metadata[0].name
    annotations = {
      "tailscale.com/tags"   = "tag:k8s,tag:public-access-allowed"
      "tailscale.com/funnel" = "true"
    }
  }
  spec {
    ingress_class_name = "tailscale"
    tls {
      hosts = ["sales-forecaster"]
    }
    rule {
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = kubernetes_service.model_service.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}
