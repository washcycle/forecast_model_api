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

- `/`
  - `/input` (input data)
  - `/model` (compiled models)
  - `/output` (model output data)
  - `/tests` (any unittest)
  - `/src` (source code for model deployment)
  - `/analysis` (any interactive jupyter notebook or other exploratory work)

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

# Deployment

- Multistage docker image, build .venv and conly copy required files and no build utils.

# Contributions

Commits use https://www.conventionalcommits.org/en/v1.0.0/
