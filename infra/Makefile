# Default values (can be overridden)
CLUSTER_CONTEXT ?= peace-kingdom
MINIKUBE_PROFILE ?= forecast-model-cluster

minikube:
	@echo "Installing minikube and starting $(MINIKUBE_PROFILE)..."
	@if minikube status -p $(MINIKUBE_PROFILE) | grep -q "Running"; then \
		echo "Minikube cluster '$(MINIKUBE_PROFILE)' is already running."; \
	else \
		curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64; \
		sudo install minikube-linux-amd64 /usr/local/bin/minikube; \
		rm minikube-linux-amd64; \
		minikube start -p $(MINIKUBE_PROFILE); \
		kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml; \
	fi

install-tailscale-operator:
	@echo "Installing Tailscale Operator via Helm..."	
	helm repo add tailscale https://pkgs.tailscale.com/helmcharts
	helm repo update
	helm upgrade --install tailscale-operator tailscale/tailscale-operator \
	  --namespace tailscale --create-namespace \
	  --set oauth.clientId=$(TS_CLIENT_ID) \
	  --set oauth.clientSecret=$(TS_CLIENT_SECRET) \
	  --set operatorConfig.hostname=$(CLUSTER_CONTEXT) \
	  --set-string apiServerProxyConfig.mode="true" \
	  --wait
	@if ! command -v tailscale >/dev/null 2>&1; then \
		echo "Tailscale is not installed, skipping kubeconfig"; \
	else \
		tailscale configure kubeconfig $(CLUSTER_CONTEXT); \
	fi

apply-terraform:
	@echo "Applying Terraform deployment for FastAPI app, HPA, and Tailscale ingress..."
	cd terraform && KUBE_CONTEXT=$(CLUSTER_CONTEXT) terraform init && KUBE_CONTEXT=$(CLUSTER_CONTEXT) terraform apply -auto-approve

.PHONY: minikube install-tailscale-operator apply-terraform