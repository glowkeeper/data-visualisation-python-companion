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

---

## What columns do we have?

```python
list(df.columns)
```

Before we go any further, spend a minute looking through the column names.

### Think

If you were using Tableau, which of these fields would you expect to appear as:

- **Dimensions**
- **Measures**

Don't worry if you're unsure.

This is one of the most important ideas in Tableau.

---

## Dimensions and Measures

Tableau divides fields into two broad categories.

### Dimensions

Dimensions describe or categorise your data.

They answer questions such as:

- Who?
- What?
- Where?
- When?
- Which?

Examples from this dataset include:

- Order ID
- Customer Name
- Category
- Sub-Category
- Region
- City
- Segment
- Ship Mode
- Order Date

Notice that these are mostly labels rather than quantities.

---

### Measures

Measures are values that can be calculated.

They answer questions such as:

- How much?
- How many?
- What's the total?
- What's the average?

Examples include:

- Sales
- Profit
- Quantity
- Discount

These are the values Tableau automatically totals, averages or counts.

---

## Why does Tableau care?

Imagine we drag:

- **Category** to Columns
- **Sales** to Rows

Tableau recognises that:

- Category is a **Dimension**
- Sales is a **Measure**

It therefore groups the rows by Category before calculating the total Sales for each group.

You never have to write any code.

Python makes this process explicit.

```python
df.groupby("Category")["Sales"].sum()
```

Read it almost like English.

> Group the data by **Category**, then calculate the total **Sales** for each group.

That is exactly what Tableau has been doing for you behind the scenes.

---

### A useful way to remember

Dimensions answer:

> **What?**

Measures answer:

> **How much?**

Think of a supermarket.

**Milk** is a Dimension.

**£1.85** is a Measure.

One describes **what** something is.

The other describes **how much**.

---

### One final point

A field doesn't have to contain text to be a Dimension.

For example:

- Customer ID
- Order ID
- Postal Code

may all contain numbers, but they are still **Dimensions** because they identify things rather than quantities that should be added together.

This is why Tableau's distinction isn't simply **text versus number**.

It's about the purpose of the data.

---

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

