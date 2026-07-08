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

# Week 3 — Behind the Tableau Curtain

## Dashboard Storytelling

Welcome back.

Over the past two weeks we've seen how Tableau quietly:

- loads data
- recognises data types
- groups information
- filters rows
- creates charts

This week we'll ask a different question.

> **When does a collection of charts become a dashboard?**

The answer isn't "when there are enough charts."

The answer is:

> **When the charts work together to answer a question.**

---

## Every dashboard begins with a question

Imagine your manager asks:

> **How is our business performing?**

That's a huge question.

Before creating any charts we need to narrow it down.

For example:

- Which regions generate the most sales?
- Which product categories are most profitable?
- Are sales increasing over time?

Notice that each question could be answered with a different chart.

---

## Load the dataset

```python
import pandas as pd
import matplotlib.pyplot as plt

DATASET = "../../data/HighStreetRetailData.xlsx"

df = pd.read_excel(DATASET)

df.head()
```

---

## Question 1

> Which regions generate the most sales?

Let's answer that.

```python
sales_by_region = (
    df.groupby("Region")["Sales"]
      .sum()
      .sort_values(ascending=False)
)

sales_by_region
```

Now visualise it.

```python
sales_by_region.plot(kind="bar")

plt.title("Sales by Region")
plt.ylabel("Sales")
plt.tight_layout()

plt.show()
```

---

## Does this answer the question?

Yes.

But only one question.

It tells us nothing about:

- profit
- product categories
- time
- customer behaviour

One chart rarely tells the whole story.

---

## Question 2

Let's ask another question.

> Which categories generate the most profit?

```python
profit_by_category = (
    df.groupby("Category")["Profit"]
      .sum()
      .sort_values(ascending=False)
)

profit_by_category
```

```python
profit_by_category.plot(kind="bar")

plt.title("Profit by Category")
plt.ylabel("Profit")
plt.tight_layout()

plt.show()
```

---

## Two charts...

We now have:

- Sales by Region
- Profit by Category

Do we have a dashboard?

Not necessarily.

We simply have two separate charts.

A dashboard should tell one coherent story.

---

## Think

Imagine presenting these charts.

What story are they telling?

Could someone explain:

- what is happening?
- why it matters?
- what should happen next?

If not, the dashboard probably needs improving.

---

## Connecting charts together

Good dashboards encourage the viewer to move naturally between charts.

For example:

Question 1

> Which region sells the most?

leads naturally to:

Question 2

> Which categories perform well in that region?

which leads to:

Question 3

> Has performance changed over time?

Each chart builds on the previous one.

That is storytelling.

---

## Behind the Tableau Curtain

When you build a dashboard in Tableau, Tableau does not decide:

- which questions matter
- which charts belong together
- what order people should read them
- what message the dashboard communicates

Those decisions belong to the analyst.

The software helps build dashboards.

People create stories.

---

## Try it yourself

Imagine you are preparing a dashboard for the Chief Executive.

Choose **three** questions from the list below.

- Which region generates the highest sales?
- Which category generates the highest profit?
- Which month has the highest sales?
- Which customer segment performs best?

Now think:

- Which chart would answer each question?
- In what order should they appear?
- Why?

Remember:

A dashboard is not simply a collection of charts.

It is a sequence of ideas.

---

## Extension Challenge

Create one additional chart.

Then write two short sentences.

**Sentence 1**

> This chart shows...

**Sentence 2**

> This matters because...

If you struggle with the second sentence, ask yourself:

> Was this the right chart to create?

---

## Reflection

This week we've moved beyond creating charts.

We've started thinking about communication.

A good dashboard should:

- answer a clear question
- avoid unnecessary information
- guide the viewer naturally
- connect charts into a coherent narrative
- support decision making

Tableau provides excellent tools for building dashboards.

Python helps us understand the analytical work that sits behind them.

Neither tool tells the story.

That remains the responsibility of the analyst.
