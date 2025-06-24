import os
from datetime import datetime

import lightgbm as lgb
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel, Field, field_validator

# Valid Store IDs and Item IDs for validation
# Could fetch this externally, but for simplicity, we define them here.
# Also the fetch could slow startup time and depending on latency and throughput requirements might be suboptimal
VALID_STORE_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
VALID_ITEM_IDS = list(range(1, 51))


# Define input schema
class ForecastInput(BaseModel):
    date: datetime = Field(examples=["2013-01-01"], description="Date for the forecast")
    store: int = Field(examples=VALID_STORE_IDS, description="Store ID")
    item: int = Field(examples=VALID_ITEM_IDS[:3], description="Item ID")

    @field_validator("store")
    @classmethod
    def validate_store(cls, value):
        if value not in VALID_STORE_IDS:
            raise ValueError(f"Invalid store ID: {value}")
        return value

    @field_validator("item")
    @classmethod
    def validate_item(cls, value):
        if value not in VALID_ITEM_IDS:
            raise ValueError(f"Invalid item ID: {value}")
        return value


# Get model (update path if needed), raise error if not found
MODEL_PATH = os.environ.get("MODEL_PATH")
print(f"Using model path: {MODEL_PATH}")
if not MODEL_PATH or not os.path.isfile(MODEL_PATH):
    raise ValueError(f"Model path is invalid or file does not exist: {MODEL_PATH}")


# The linters like this to a dict type
resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    try:
        resources["model"] = lgb.Booster(model_file=MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to load model from {MODEL_PATH}: {e}")
    resources["status"] = "ready"
    yield
    resources["status"] = None


app = FastAPI(lifespan=lifespan)


@app.post("/predict")
def forecast(input: ForecastInput, version: str = "v1"):
    if version != "v1":
        return HTTPException(
            status_code=404, detail=f"Unsupported API version: {version}"
        )

    if version == "v1":
        return _version_v1(input)


def _version_v1(input):
    features = {
        "store": input.store,
        "item": input.item,
        "month": input.date.month,
        "day": input.date.weekday(),
        "year": input.date.year,
    }

    try:
        X = pd.DataFrame([features])
    except Exception as e:
        raise ValueError(f"Failed to create DataFrame from input: {e}")

    try:
        y_pred = resources["model"].predict(X)[0]
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {e}")

    return {"sales": y_pred}


@app.get("/status")
def health():
    if resources.get("status"):
        return resources.get("status")
    else:
        return {"status": "not ready"}
