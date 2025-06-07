import os
from datetime import datetime

import lightgbm as lgb
import pandas as pd
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel, Field, field_validator

# Valid Store IDs and Item IDs for validation
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


# Load model (update path if needed)
MODEL_PATH = os.environ.get("MODEL_PATH") or os.path.join(
    os.path.dirname(__file__), "lgbm_model.txt"
)
if not MODEL_PATH or not os.path.isfile(MODEL_PATH):
    raise ValueError(f"Model path is invalid or file does not exist: {MODEL_PATH}")

# The linters like this to a dict type
resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    resources["model"] = lgb.Booster(model_file=MODEL_PATH)
    resources["status"] = "ready"
    yield
    resources["status"] = None


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
    if resources.get("status"):
        return resources.get("status")
    else:
        return {"status": "not ready"}
