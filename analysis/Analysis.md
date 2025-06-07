


Workbook Fixes

It's an older challenge so the code the packages are a bit dated with some breaking changes. I made the following to address those issues.

While the code didn't use prohet I took the liberty to make it compatible with the current package.

```python
# Latest Version of Prophet uses prophet not fbprophet for import (add this try except for backward compatibility)
try:
    from fbprophet import Prophet
except ImportError:
    from prophet import Prophet
```

Updated the values parameter because date threw an excpetion as it wasn't numeric, can't take the mean of a string.

```python
# Let us understand the sales data distribution across the stores
def sales_data_understanding(data: pd.DataFrame):
    store_df = data.copy()
    plt.figure(figsize=(20, 10))
    sales_pivoted_df = pd.pivot_table(
        store_df,
        index="store",
        values=["sales"], # had to remove "date" as it is not a numeric value
        columns="item",
        aggfunc=np.mean,
    )
    sales_pivoted_df.plot(kind="hist", figsize=(20, 10))
    # Pivoted dataframe
    display(sales_pivoted_df)
    return (store_df, sales_pivoted_df)
```



Animated (# Scatter plot of average sales per store) by year, used GitHub Copilot to generate that part. Not a huge fan of displaying the sales like this, i'd rather plot something that captures the trend over time in a more intuative way.

Something that came to mind while looking at the provider notebook, is that sales for items could be correlated either positively or inversly so it could be possibe to add more relveant information for the model to train on using the cross-correlated items. 

## LightGBM

Encountered `TypeError: train() got an unexpected keyword argument 'early_stopping_rounds'`

New LightGBM doesn't have that available on the `train` call it was moved to `callbacks` parameters like so:

```python
callbacks=[
    lgb.early_stopping(stopping_rounds=3),
    lgb.log_evaluation(period=50),
],
```

# Modeling Training Feedback

I didn't see any hyper parameter tuning, i'd setup a regime to intelligently sweep parameters like bayseian optimization.