import os
from datetime import datetime

import lightgbm as lgb
import pandas as pd
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel, Field


# Define input schema
class ForecastInput(BaseModel):
    date: datetime = Field(json_schema_extra={"example": "2013-01-01"})
    store: int = Field()
    item: int = Field()


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
    features = {
        "store": input.store,
        "item": input.item,
        "month": input.date.month,
        "day": input.date.weekday(),
        "year": input.date.year,
    }
    X = pd.DataFrame([features])
    y_pred = resources["model"].predict(X)[0]
    return {"sales": y_pred}


@app.get("/status")
def health():
    if status is None:
        return {"status": "not ready"}
    return {"status": status}
