---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: 1.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Week 2 --- Behind the Tableau Curtain

## Filtering, Sorting and Grouping Data

Welcome back!

Last week we discovered that Tableau quietly:

-   loaded our spreadsheet
-   recognised data types
-   separated **Dimensions** from **Measures**

This week we'll explore another important question:

> **How does Tableau know which data to show?**

Every time you drag a field into Filters, click Sort, or build a chart,
Tableau performs operations on your data.

Python simply makes those operations visible.

------------------------------------------------------------------------

## Load the dataset

``` python
import pandas as pd

DATASET = "../../data/HighStreetRetailData.xlsx"

df = pd.read_excel(DATASET)

df.head()
```

------------------------------------------------------------------------

## Looking at all the data

Very rarely do we want to analyse *everything* at once.

Filtering helps us focus on the data that answers our question.

------------------------------------------------------------------------

## Filtering rows

``` python
south = df[df["Region"] == "South"]

south.head()
```

Read this almost like English.

> Keep only the rows where **Region** equals **South**.

This is exactly what Tableau does when you drag **Region** onto the
Filters shelf.

------------------------------------------------------------------------

## Try it yourself

Filter for:

-   North
-   East
-   West

How many rows are returned?

``` python
south.shape
```

------------------------------------------------------------------------

## Grouping

Filtering changes **which rows** we analyse.

Grouping changes **how rows are organised**.

``` python
sales = (
    df.groupby("Category")["Sales"]
      .sum()
)

sales
```

This is equivalent to placing:

-   Category on Columns
-   Sales on Rows

inside Tableau.

------------------------------------------------------------------------

## Sorting

``` python
sales.sort_values(ascending=False)
```

Sorting often makes comparisons easier.

Think about what happens when you click the Sort button in Tableau.

------------------------------------------------------------------------

## Creating a chart

``` python
import matplotlib.pyplot as plt

sales.sort_values(ascending=False).plot(kind="bar")

plt.title("Sales by Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.show()
```

------------------------------------------------------------------------

## Behind the Tableau Curtain

This week Tableau quietly:

-   filtered rows
-   grouped records
-   calculated totals
-   sorted results
-   created a chart

Python simply makes each of those operations explicit.

------------------------------------------------------------------------

## Challenge

1.  Filter to a single Region.
2.  Group by Sub-Category.
3.  Calculate total Profit.
4.  Sort the results.
5.  Create a bar chart.

Experiment. Small changes are one of the best ways to learn Python.

------------------------------------------------------------------------

## Reflection

Tableau gives us a powerful graphical interface.

Python asks us to describe the same analytical operations using code.

As you become comfortable with both tools, you'll realise they are
solving exactly the same problems---just in different ways.
