---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: "1.3"
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Week 4 — Behind the Tableau Curtain

## Forecasting with Python

This week Tableau lets us drag **Forecast** onto a time-series chart.

The result appears quickly:

- a line extends into the future
- a shaded band represents uncertainty
- Tableau chooses a forecasting model

That convenience is useful, but it hides an important analytical question:

> **What assumptions turned past data into this possible future?**

Python makes those assumptions visible.

This is not a lesson in becoming a forecasting programmer. It is an
analytical conversation about when a forecast deserves to influence a
decision.

---

## A forecast is not a fact

A forecast is an estimate based on:

- the historical data available
- the pattern a model looks for
- the period being predicted
- an assumption that some part of the past remains useful

Different reasonable models can produce different futures from the same
data.

Our job is therefore not merely to generate a forecast.

Our job is to ask:

> **Would this forecast have been useful before we knew what happened?**

---

## Load the retail data

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

DATASET = "../../data/HighStreetRetailData.xlsx"

df = pd.read_excel(DATASET)

df[["Order Date", "Sales", "Profit"]].head()
```

---

## Tableau needs a time series

The spreadsheet contains individual orders.

A forecasting model needs observations arranged at consistent time
intervals. We will reproduce the effect of placing:

- `MONTH(Order Date)` on Columns
- `SUM(Sales)` on Rows

in Tableau.

```python
monthly_sales = (
    df.set_index("Order Date")["Sales"]
      .resample("MS")
      .sum()
      .rename("Sales")
      .to_frame()
)

monthly_sales.head()
```

`MS` means **month start**. Each row now represents one complete month.

This aggregation is an analytical decision. Daily, monthly and yearly
data can reveal very different patterns.

---

## Check the structure before forecasting

```python
expected_months = pd.date_range(
    monthly_sales.index.min(),
    monthly_sales.index.max(),
    freq="MS",
)

missing_months = expected_months.difference(monthly_sales.index)

print(f"Months available: {len(monthly_sales)}")
print(f"First month: {monthly_sales.index.min():%B %Y}")
print(f"Last month: {monthly_sales.index.max():%B %Y}")
print(f"Missing months: {len(missing_months)}")
```

A regular monthly sequence does not guarantee a reliable forecast, but
missing intervals would give us an immediate reason to investigate.

In Tableau, this is why the date level and continuous axis matter.

---

## What pattern do we see?

```python
fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(
    monthly_sales.index,
    monthly_sales["Sales"],
    color="#365f91",
    marker="o",
    linewidth=2,
)

ax.set_title("Monthly Sales")
ax.set_xlabel("")
ax.set_ylabel("Sales")
ax.grid(axis="y", alpha=0.25)

plt.tight_layout()
plt.show()
```

Before running a model, look at the evidence.

Think:

- Is there an overall direction?
- Do some months appear regularly higher than others?
- Is the variation stable?
- Would one unusual month distort our judgement?

---

## Test before trusting

If we fit a model to every month and then inspect how closely it follows
those same months, we have not tested its ability to predict.

Instead, we will hide the final six months:

- the earlier months become the **training period**
- the hidden months become the **test period**

This simulates making a forecast before those six months occurred.

```python
monthly_sales["Month number"] = np.arange(len(monthly_sales))

train = monthly_sales.iloc[:-6].copy()
test = monthly_sales.iloc[-6:].copy()

print(f"Training period ends: {train.index.max():%B %Y}")
print(f"Test period: {test.index.min():%B %Y} to {test.index.max():%B %Y}")
```

This simple step reveals something a finished forecast chart can hide:

> A useful model should be judged on data it did not use to learn.

---

## Model 1 — Continue the overall trend

A linear trend assumes that Sales change by approximately the same amount
each month.

```python
trend_model = LinearRegression()

trend_model.fit(
    train[["Month number"]],
    train["Sales"],
)

test["Trend forecast"] = trend_model.predict(
    test[["Month number"]]
)

test[["Sales", "Trend forecast"]]
```

The model is mathematically simple:

> start from a baseline and add a similar amount each month

That may be reasonable—or completely inappropriate. The code forces us
to name the assumption.

---

## Compare the trend with what happened

```python
fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(
    train.index,
    train["Sales"],
    color="#8c8c8c",
    label="Training data",
)
ax.plot(
    test.index,
    test["Sales"],
    color="#222222",
    marker="o",
    linewidth=2,
    label="Actual test data",
)
ax.plot(
    test.index,
    test["Trend forecast"],
    color="#d95f02",
    marker="o",
    linestyle="--",
    linewidth=2,
    label="Trend forecast",
)

ax.axvline(test.index.min(), color="#666666", linestyle=":", alpha=0.8)
ax.set_title("Could a Simple Trend Predict the Final Six Months?")
ax.set_xlabel("")
ax.set_ylabel("Sales")
ax.grid(axis="y", alpha=0.25)
ax.legend()

plt.tight_layout()
plt.show()
```

The forecast captures a broad direction, but it misses much of the
month-to-month variation.

Is that accurate enough to support an inventory or staffing decision?

We need a measure, not just an impression.

---

## Measure the error

We will use **Mean Absolute Error (MAE)**.

It answers:

> On average, how far was the forecast from the actual monthly Sales?

```python
trend_mae = mean_absolute_error(
    test["Sales"],
    test["Trend forecast"],
)

print(f"Trend forecast MAE: {trend_mae:,.0f}")
```

Lower is better, but an error value has meaning only in context.

An average error of 25,000 might be tolerable for one decision and
unacceptable for another.

---

## Model 2 — Repeat last year's seasonal pattern

Retail data may be seasonal. November this year may resemble November
last year more than it resembles October this year.

A simple seasonal forecast says:

> Use the Sales from the same month one year earlier.

```python
monthly_sales["Seasonal forecast"] = monthly_sales["Sales"].shift(12)

test["Seasonal forecast"] = monthly_sales.loc[
    test.index,
    "Seasonal forecast",
]

test[["Sales", "Trend forecast", "Seasonal forecast"]]
```

This is still an assumption.

It assumes that last year's monthly pattern remains informative.

---

## Compare the two models

```python
seasonal_mae = mean_absolute_error(
    test["Sales"],
    test["Seasonal forecast"],
)

model_comparison = pd.DataFrame(
    {
        "Model": ["Linear trend", "Same month last year"],
        "Mean absolute error": [trend_mae, seasonal_mae],
    }
).sort_values("Mean absolute error")

model_comparison
```

```python
fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(
    test.index,
    test["Sales"],
    color="#222222",
    marker="o",
    linewidth=2.5,
    label="Actual Sales",
)
ax.plot(
    test.index,
    test["Trend forecast"],
    color="#d95f02",
    marker="o",
    linestyle="--",
    label="Linear trend",
)
ax.plot(
    test.index,
    test["Seasonal forecast"],
    color="#1b9e77",
    marker="o",
    linestyle="--",
    label="Same month last year",
)

ax.set_title("Two Reasonable Models, Two Different Forecasts")
ax.set_xlabel("")
ax.set_ylabel("Sales")
ax.grid(axis="y", alpha=0.25)
ax.legend()

plt.tight_layout()
plt.show()
```

For this six-month test, the seasonal baseline has the lower error.

That does not prove it will always be best. It demonstrates why analysts
compare plausible models instead of trusting the first forecast produced.

---

## Behind the Tableau Curtain

Tableau can automatically look for trend and seasonal patterns. Its
forecasting system is more sophisticated than either of our simple
examples.

But Tableau still has to make choices about:

- the time interval
- trend
- seasonality
- forecast horizon
- uncertainty

Python has not given us a universally better forecast.

It has made the competing assumptions visible.

---

## Forecast the next six months

We will now refit the trend model using all available months and compare
its future values with the seasonal baseline.

```python
final_trend_model = LinearRegression()

final_trend_model.fit(
    monthly_sales[["Month number"]],
    monthly_sales["Sales"],
)

future_dates = pd.date_range(
    monthly_sales.index.max() + pd.offsets.MonthBegin(1),
    periods=6,
    freq="MS",
)

future = pd.DataFrame(index=future_dates)
future["Month number"] = np.arange(
    len(monthly_sales),
    len(monthly_sales) + len(future),
)

future["Trend forecast"] = final_trend_model.predict(
    future[["Month number"]]
)

last_year_sales = monthly_sales["Sales"].iloc[-12:-6].to_numpy()
future["Seasonal forecast"] = last_year_sales

future
```

These forecasts answer the same question with different assumptions.

Neither should be presented as certain.

---

## Add an uncertainty band

The trend model's past errors give us a rough indication of how variable
its predictions have been.

The interval below is deliberately labelled **illustrative**. It is not
Tableau's confidence interval and it does not account for every source of
risk.

```python
fitted_history = final_trend_model.predict(
    monthly_sales[["Month number"]]
)

residuals = monthly_sales["Sales"] - fitted_history
illustrative_margin = 1.28 * residuals.std()

future["Lower illustrative bound"] = (
    future["Trend forecast"] - illustrative_margin
).clip(lower=0)

future["Upper illustrative bound"] = (
    future["Trend forecast"] + illustrative_margin
)
```

```python
recent_history = monthly_sales.iloc[-24:]

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    recent_history.index,
    recent_history["Sales"],
    color="#365f91",
    marker="o",
    linewidth=2,
    label="Historical Sales",
)
ax.plot(
    future.index,
    future["Trend forecast"],
    color="#d95f02",
    marker="o",
    linestyle="--",
    linewidth=2,
    label="Trend forecast",
)
ax.plot(
    future.index,
    future["Seasonal forecast"],
    color="#1b9e77",
    marker="o",
    linestyle="--",
    linewidth=2,
    label="Seasonal forecast",
)
ax.fill_between(
    future.index,
    future["Lower illustrative bound"],
    future["Upper illustrative bound"],
    color="#d95f02",
    alpha=0.15,
    label="Illustrative trend uncertainty",
)

ax.axvline(future.index.min(), color="#666666", linestyle=":")
ax.set_title("The Future Depends on the Assumption")
ax.set_xlabel("")
ax.set_ylabel("Sales")
ax.grid(axis="y", alpha=0.25)
ax.legend()

plt.tight_layout()
plt.show()
```

The shaded area is not a promise that the future will fall inside it.

It communicates that a forecast without uncertainty is incomplete.

---

## Think like an analyst

Imagine the seasonal forecast predicts a strong November.

Before recommending additional inventory, ask:

- Was last November affected by a promotion?
- Have prices or product ranges changed?
- Could supply problems limit Sales?
- Is the forecast accurate enough for the cost of the decision?
- What happens if demand falls outside the expected range?

The model knows only the information represented in its data.

It does not know that the business environment has changed unless that
change is measured and included.

---

## Try it yourself — Forecast Profit

Repeat the analytical process for monthly Profit.

You do not need to write a new modelling system. Change the measure,
rerun the comparison and ask:

- Is Profit more or less predictable than Sales?
- Does the trend model or seasonal baseline perform better?
- Would a Sales forecast alone support a good decision?

Start by creating the monthly series:

```python
monthly_profit = (
    df.set_index("Order Date")["Profit"]
      .resample("MS")
      .sum()
      .rename("Profit")
      .to_frame()
)

monthly_profit.head()
```

---

## Decision

Suppose you must advise HighStreet Retail about stock and staffing for
the next six months.

Write three short statements:

1. **Prediction:** What might happen?
2. **Uncertainty:** Why might the forecast be wrong?
3. **Decision:** What cautious action would you recommend?

A strong recommendation does not hide uncertainty.

It explains how the decision should respond to it.

---

## Reflection

This week Tableau generated forecasts quickly.

Python exposed the analytical work underneath:

- choosing a time interval
- checking data structure
- withholding data for testing
- naming a model's assumption
- comparing plausible models
- measuring forecast error
- communicating uncertainty

The most important lesson is not that Python is better than Tableau.

It is this:

> **A forecast deserves influence only when its assumptions, errors and
> uncertainty are understood well enough for the decision being made.**
