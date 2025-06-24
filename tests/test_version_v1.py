# Test for version 1 of the forecasting API
def test_version_v1():
    from app import _version_v1, resources, ForecastInput    
    import pandas as pd
    import lightgbm as lgb

    # Mock the model loading
    resources["model"] = lgb.Booster(model_file="tests/test_lgbm_model_v1.txt")
    resources["status"] = "ready"

    # Create a sample input
    input_data = ForecastInput(
        store=1,
        item=1,
        date=pd.Timestamp("2023-10-01")
    )

    # Call the version 1 function
    response = _version_v1(input_data)

    # Check the response structure
    assert "sales" in response
    assert isinstance(response["sales"], float)