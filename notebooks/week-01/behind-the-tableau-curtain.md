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

# Week 1 — Behind the Tableau Curtain

## Exploring Data with pandas

Welcome!

This notebook is an optional companion to Week 1.

+++

## Step 1 — Import pandas

`pandas` is the most popular Python library for working with tabular data.

```python
import pandas as pd
```

+++

## Step 2 — Load the dataset

```python
DATASET = "../../data/HighStreetRetailData.xlsx"

df = pd.read_excel(DATASET)

df.head()
```

+++

## What did we just load?

Before making charts ask yourself:

- What does one row represent?
- What information is available?
- Which columns contain numbers?
- Which columns contain categories?

+++

## How big is our dataset?

```python
df.shape
```

+++

`shape` returns:

```text
(rows, columns)
```

Think:

- Is this a large dataset?
- What if it contained ten million rows?

+++

## What columns do we have?

```python
list(df.columns)
```

+++

### Try it yourself

Which columns would Tableau probably treat as:

- Dimensions?
- Measures?

+++

## Data types

```python
df.info()
```

+++

## Summary statistics

```python
df.describe()
```

+++

## Grouping

```python
sales_by_category = (
    df.groupby("Category")["Sales"]
      .sum()
)

sales_by_category
```

+++

Read this like English.

> Group by Category, then total the Sales.

This is what Tableau is doing automatically.

+++

## Sorting

```python
sales_by_category.sort_values(ascending=False)
```

+++

## Chart

```python
import matplotlib.pyplot as plt

sales_by_category.sort_values(
    ascending=False
).plot(kind="bar")

plt.title("Sales by Category")
plt.tight_layout()
plt.show()
```

+++

## Behind the Tableau Curtain

Today Tableau:

- loaded the spreadsheet
- recognised data types
- grouped data
- calculated totals
- sorted results
- produced a chart

Python makes each step explicit.

+++

## Extension Challenge

1. Replace **Category** with **Region**.
2. Replace **Sales** with **Profit**.
3. What changes?

