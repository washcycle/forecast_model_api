# Store Item Demand Forecasting

Project seeks to build upon the data and model from the Store Item Demand Forecasting Challenge.

[Data] (https://www.kaggle.com/c/demand-forecasting-kernels-only/data)
[Model Notebook](https://www.kaggle.com/code/ashishpatel26/light-gbm-demand-forecasting/notebook)

## Prerequisites

- Kaggle Account
- Setup kaggle cli  `pip install kaggle`
- Create API toekn in `https://www.kaggle.com/settings`
- Python enviornment

## Project Structure

To keep things tidy the project structure is split by funtion:

- `./`
  - `./input` (input data)
  - `./model` (compiled models)
  - `./output` (model output data)
  - `./tests` (any unittest)
  - `./src` (source code for model deployment)
  - `./analysis` (any interactive jupyter notebook or other exploratory work)
  - `./infra` (any project specific deployment code)

# Data

```bash
kaggle competitions download -c demand-forecasting-kernels-only` 
unzip demand-forecasting-kernels-only.zip  -d inputs
```

# Steps

- Fixed Facebook Prohet import in jupyter notebook
- Created multistage docker container to minimize container footprint. This helps scale up deployments faster in a container ochestrators.
- Wrapped latest FastAPI version around model and created predict endpoints.
- Add isort to organize imports and ran on the src and analysis directory.

## Model Deployment

k8s is a common container orchestrator witha healthy ecosystem.

For repeatability and demo purposes I used minikube with Tailscale ingress to deploy the model and makei t accesible to the public internet. This can also be restirtied to a intranet as well.

The `infra` folder contains a makefile that creates a minikube cluster and sets up the tailscale operator.

The operator can deploy ingress to your tailnet, and there is a flag to make them `funnel` for public access.

*Install minikube and create cluster for this project*
`make minikube`

*Install the Tailscale operator*
`TS_CLIENT_ID=your_client_id TS_CLIENT_SECRET=your_client_secret make install-tailscale-operator`

Used terraform for IaC (Infrastructure as Code) to deploy the model inside the local minikube cluster. Since this is a public repo, the image doens't need authentication to pull, but I added terraform to show how pull secrets can be used for private registries.

## API

https://sales-forecaster.tigris-vibes.ts.net/

**API Docs**

https://sales-forecaster.tigris-vibes.ts.net/docs

API Predict

https://sales-forecaster.tigris-vibes.ts.net/predict

API Status 

https://sales-forecaster.tigris-vibes.ts.net/status

## API Features

*Input validation:* Item ID and Store ID validation based on what was in the trianing data, withh response with proper errors messages if ID exceeds allowed values.

Exampe:

*Input*
```json
{
  "date": "2017-01-01",
  "store": 1000,
  "item": 1000
}
```

*Response*
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body",
        "store"
      ],
      "msg": "Value error, Invalid store ID: 1000",
      "input": 1000,
      "ctx": {
        "error": {}
      }
    },
    {
      "type": "value_error",
      "loc": [
        "body",
        "item"
      ],
      "msg": "Value error, Invalid item ID: 1000",
      "input": 1000,
      "ctx": {
        "error": {}
      }
    }
  ]
}
```

# Contributions

Commits use https://www.conventionalcommits.org/en/v1.0.0/
