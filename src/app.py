import os
from datetime import datetime

import lightgbm as lgb
import pandas as pd
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel


# Define input schema
class ForecastInput(BaseModel):
    date: str
    store: int
    item: int


# Load model (update path if needed)
MODEL_PATH = os.environ.get("MODEL_PATH") or os.path.join(
    os.path.dirname(__file__), "lgbm_model.txt"
)
if not MODEL_PATH or not os.path.isfile(MODEL_PATH):
    raise ValueError(f"Model path is invalid or file does not exist: {MODEL_PATH}")

# The linters like this to a dict type
resources = {}

# Global variable to track the status of the API
status = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    resources["model"] = lgb.Booster(model_file=MODEL_PATH)
    status = "ready"
    yield
    status = None


app = FastAPI(lifespan=lifespan)


@app.post("/predict")
def forecast(input: ForecastInput):
    dt = datetime.strptime(input.date, "%Y-%m-%d")
    features = {
        "store": input.store,
        "item": input.item,
        "month": dt.month,
        "day": dt.weekday(),
        "year": dt.year,
    }
    X = pd.DataFrame([features])
    # TODO: Replace with actual model prediction
    y_pred = resources["model"].predict(X)[0]
    y_pred = 0  # Dummy value
    return {"sales": y_pred}


@app.get("/status")
def health():
    if status is None:
        return {"status": "not ready"}
    return {"status": status}
