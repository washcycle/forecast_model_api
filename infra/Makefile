minikube:
	@echo "Installing minikube and starting forecast_model_cluster..."
	@if minikube status -p forecast-model-cluster | grep -q "Running"; then \
		echo "Minikube cluster 'forecast-model-cluster' is already running."; \
	else \
		curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64; \
		sudo install minikube-linux-amd64 /usr/local/bin/minikube; \
		rm minikube-linux-amd64; \
		minikube start -p forecast-model-cluster; \
		# Install some addons; \
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
	  --set operatorConfig.hostname=peace-kingdom \
	  --set-string apiServerProxyConfig.mode="true" \
	  --wait
	tailscale configure kubeconfig peace-kingdom

apply-terraform:
	@echo "Applying Terraform deployment for FastAPI app, HPA, and Tailscale ingress..."
	cd terraform && terraform init && terraform apply -auto-approve
	
.PHONY: minikube install-tailscale-operator apply-terraform
