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

# Week 5 — Behind the Tableau Curtain

## Accessible and Responsible Visualisation

This week, Tableau helps us improve:

- colour
- labels
- layout
- trend lines
- forecasts

But the software cannot decide whether a visualisation is fair, clear or
accessible.

Those decisions belong to the analyst.

Python makes this especially visible because every design choice must be
stated.

This is not a lesson in becoming a visualisation programmer. It is an
analytical conversation about a more important question:

> **How can the same accurate data support different—and sometimes
> misleading—interpretations?**

---

## Responsible visualisation begins before colour

A chart can be numerically accurate and still create barriers.

For example:

- an unclear title can hide the question
- colour can decorate rather than explain
- a truncated scale can exaggerate a difference
- small text can make evidence difficult to read
- a chart without a text alternative can exclude some users
- an automated output can look authoritative without being useful

Accessibility is not a decorative final step.

Responsibility is not achieved by choosing one approved colour palette.

Both require us to consider how evidence will be understood.

---

## Load the retail data

```python
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

DATASET = "../../data/HighStreetRetailData.xlsx"

df = pd.read_excel(DATASET)

df[["Category", "Sales", "Profit"]].head()
```

---

## Check the categories before drawing

Charts are often trusted because they look polished.

Before choosing colours or labels, we should check that the chart
structure represents the data correctly.

```python
categories = sorted(df["Category"].dropna().unique())

print(f"Number of categories: {len(categories)}")
print("Valid category values:")

for category in categories:
    print(f"- {category}")
```

The dataset contains three valid Category values:

- Furniture
- Office Supplies
- Technology

This matters. A visually impressive chart is still wrong if it mixes
Category and Sub-Category values under one label.

> **Accuracy comes before aesthetics.**

---

## Build one shared evidence table

We will use the same totals throughout the notebook.

That lets us separate two questions:

1. What does the data say?
2. How does the design influence what the viewer notices?

```python
category_performance = (
    df.groupby("Category", as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Profit=("Profit", "sum"),
      )
      .sort_values("Sales", ascending=False)
      .reset_index(drop=True)
)

category_performance
```

This table is useful in its own right.

It provides:

- exact values
- meaningful row and column headings
- information that does not depend on colour

A chart and an accessible table can complement each other. They do not
have to compete.

---

## First design — colour without purpose

The code below uses:

- a different colour for every bar
- a generic title
- no direct value labels
- visual effects that do not explain the evidence

The data remains correct.

```python
fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(
    category_performance["Category"],
    category_performance["Sales"],
    color=["#e41a1c", "#4daf4a", "#377eb8"],
    edgecolor="black",
    hatch=["///", "\\\\\\", "xxx"],
)

ax.set_title("Sales by Category")
ax.set_xlabel("Category")
ax.set_ylabel("Sales")
ax.grid(axis="y", alpha=0.45)

plt.tight_layout()
plt.show()
```

The hatching means that colour is not the only difference between bars.
That helps some viewers, but it does not give the colours an analytical
purpose.

Think:

- What should the viewer notice first?
- Why does each category need a different colour?
- Can the exact values be recovered easily?
- Does the title communicate an insight—or merely name the fields?

---

## Design is a hierarchy of attention

Suppose the decision-maker needs to understand which category generates
the most Sales.

Now the design has a clear job:

> **Make the leading category easy to identify without hiding the
> others.**

We will:

- sort the bars
- use neutral colour for context
- highlight only the leading category
- label every value directly
- state the insight in the title

```python
sales_chart = category_performance.sort_values(
    "Sales",
    ascending=True,
).copy()

leading_category = sales_chart.loc[
    sales_chart["Sales"].idxmax(),
    "Category",
]

sales_chart["Colour"] = sales_chart["Category"].map(
    lambda category: "#c55a11" if category == leading_category else "#b7b7b7"
)

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.barh(
    sales_chart["Category"],
    sales_chart["Sales"],
    color=sales_chart["Colour"],
)

ax.bar_label(
    bars,
    labels=[f"£{value / 1000:,.0f}k" for value in sales_chart["Sales"]],
    padding=5,
)

ax.set_title(
    f"{leading_category} Generates the Highest Sales",
    loc="left",
    fontweight="bold",
)
ax.set_xlabel("Sales")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(
    FuncFormatter(lambda value, _: f"£{value / 1000:,.0f}k")
)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
```

The highlight is helpful, but it is not carrying the meaning alone.

The leading category is also communicated through:

- position
- sorting
- a direct label
- an insight-led title

> **Colour reinforces the message. It does not contain the message.**

---

## Provide the insight without the chart

An accessible visualisation should not assume that every user can inspect
the image in the same way.

We can generate a concise text summary from the same evidence.

```python
leader = category_performance.iloc[0]
runner_up = category_performance.iloc[1]

sales_difference = leader["Sales"] - runner_up["Sales"]
sales_difference_pct = sales_difference / runner_up["Sales"] * 100

sales_summary = (
    f"{leader['Category']} generated the highest Sales at "
    f"£{leader['Sales']:,.0f}. This was £{sales_difference:,.0f} "
    f"({sales_difference_pct:.1f}%) more than "
    f"{runner_up['Category']}, the next-highest category."
)

print(sales_summary)
```

This summary is not a replacement for every chart.

It is another route to the key evidence.

It can be used as:

- nearby explanatory text
- a chart caption
- the basis of useful alt text
- a starting point for a spoken explanation

Useful alt text communicates the chart's purpose and main finding. It
does not need to describe every decorative detail.

---

## A responsible design check

We can record some design decisions as data.

This does not prove that a chart is accessible. It creates a visible
checklist that makes omissions easier to discuss.

```python
design_check = pd.Series(
    {
        "Uses valid categories": True,
        "Insight stated in title": True,
        "Meaning does not depend on colour": True,
        "Values labelled directly": True,
        "Readable text used": True,
        "Text summary or table available": True,
        "Scale begins at zero": True,
        "Important context explained": False,
    },
    name="Check passed",
)

design_check.to_frame()
```

One item remains false:

> **Important context explained**

The chart shows which category has the highest Sales, but not:

- whether high Sales produced high Profit
- whether performance is improving
- how uncertain future performance may be
- what action the business should take

A checklist can prompt judgement.

It cannot replace judgement.

---

## Accurate values, misleading scale

Responsible design also means avoiding visual exaggeration.

The next two charts use exactly the same Sales totals.

Only the vertical scale changes.

```python
comparison = category_performance.sort_values("Sales", ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

for ax in axes:
    bars = ax.bar(
        comparison["Category"],
        comparison["Sales"],
        color="#6b8e9f",
    )
    ax.bar_label(
        bars,
        labels=[f"£{value / 1000:,.0f}k" for value in comparison["Sales"]],
        padding=4,
    )
    ax.set_ylabel("Sales")
    ax.tick_params(axis="x", rotation=15)
    ax.spines[["top", "right"]].set_visible(False)

axes[0].set_title("Fair Comparison: Scale Starts at Zero")
axes[0].set_ylim(0, comparison["Sales"].max() * 1.15)

axes[1].set_title("Exaggerated Comparison: Truncated Scale")
axes[1].set_ylim(
    comparison["Sales"].min() * 0.95,
    comparison["Sales"].max() * 1.03,
)

plt.tight_layout()
plt.show()
```

Both charts display the same values.

The truncated scale makes the difference appear much larger.

For a bar chart, length encodes value. Removing the zero baseline
distorts that encoding.

Think:

- How might the second chart influence a hurried decision-maker?
- Does adding exact labels make the truncated scale acceptable?
- When would a line chart legitimately use a non-zero scale?

The responsible question is not merely:

> **Is the chart technically possible?**

It is:

> **Does the design represent the importance of the difference fairly?**

---

## Sales alone can produce an incomplete decision

The Sales chart places Technology first.

But a decision based only on Sales could ignore profitability.

```python
profit_chart = category_performance.sort_values(
    "Profit",
    ascending=True,
).copy()

lowest_profit_category = profit_chart.loc[
    profit_chart["Profit"].idxmin(),
    "Category",
]

profit_chart["Colour"] = profit_chart["Category"].map(
    lambda category: (
        "#c55a11"
        if category == lowest_profit_category
        else "#b7b7b7"
    )
)

fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.barh(
    profit_chart["Category"],
    profit_chart["Profit"],
    color=profit_chart["Colour"],
)

ax.bar_label(
    bars,
    labels=[f"£{value / 1000:,.0f}k" for value in profit_chart["Profit"]],
    padding=5,
)

ax.set_title(
    f"{lowest_profit_category} Generates the Lowest Profit",
    loc="left",
    fontweight="bold",
)
ax.set_xlabel("Profit")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(
    FuncFormatter(lambda value, _: f"£{value / 1000:,.0f}k")
)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
```

The design now directs attention to a different business question.

The data has not contradicted itself:

- one chart asks which category generates the most Sales
- the other asks which category generates the least Profit

Responsibility includes making the question visible.

---

## Add the missing relationship

Profit margin helps us compare Profit relative to Sales.

```python
category_performance["Profit Margin"] = (
    category_performance["Profit"]
    / category_performance["Sales"]
)

responsible_table = (
    category_performance[
        ["Category", "Sales", "Profit", "Profit Margin"]
    ]
    .sort_values("Profit Margin", ascending=False)
    .style.format(
        {
            "Sales": "£{:,.0f}",
            "Profit": "£{:,.0f}",
            "Profit Margin": "{:.1%}",
        }
    )
)

responsible_table
```

This additional measure changes the interpretation.

Think:

- Which category produces the strongest margin?
- Which category needs investigation?
- Would "invest more in the highest-Sales category" now be a sufficiently
  justified recommendation?

> **Responsible visualisation includes the context needed to avoid an
> obvious misinterpretation.**

---

## What about automated recommendations?

Software could automatically:

- sort the categories
- select a colour palette
- highlight the maximum value
- generate a title
- describe the highest and lowest figures

Those actions may save time.

But automation does not know:

- which business question matters most
- whether Sales or Profit should lead the story
- what level of difference is meaningful
- what accessibility needs the audience has
- whether important context is missing
- what decision the evidence can justify

An automated statement such as:

> **Technology is the best-performing category**

is too confident.

"Best-performing" has not been defined.

A more responsible statement would name the measure:

> **Technology generated the highest total Sales in this dataset.**

Even that statement needs context before it becomes a recommendation.

---

## Human judgement remains visible

We can let code identify numerical extremes.

```python
automated_observations = {
    "Highest Sales": category_performance.loc[
        category_performance["Sales"].idxmax(),
        "Category",
    ],
    "Highest Profit": category_performance.loc[
        category_performance["Profit"].idxmax(),
        "Category",
    ],
    "Highest Profit Margin": category_performance.loc[
        category_performance["Profit Margin"].idxmax(),
        "Category",
    ],
}

pd.Series(
    automated_observations,
    name="Category identified by code",
).to_frame()
```

The code answers three precisely defined questions.

It does not decide:

- which observation belongs on the dashboard
- why the difference exists
- whether the pattern will continue
- what the business should do

This is the same principle we applied to the Week 4 forecast:

> **Automation suggests. The analyst evaluates and decides.**

---

## Final responsibility audit

Before publishing a chart or dashboard, ask:

### Data

- Are the fields and categories represented correctly?
- Are the calculations appropriate?
- Is important context missing?

### Insight

- Is the question clear?
- Does the title state the finding accurately?
- Can the meaning be understood without colour?
- Are labels, contrast and text readable?
- Is a text summary or accessible table available where needed?
- Does the scale represent the difference fairly?
- Are limitations and uncertainty visible?

### Decision

- What decision does the visualisation support?
- Is the recommendation justified by the evidence?
- Could the design encourage an exaggerated or unfair conclusion?
- Has any automated output been checked?

Python can make these choices explicit.

It cannot make them responsible.

---

## Try it yourself

Choose one chart from your Week 5 dashboard.

Write short answers to these questions:

1. What exact question does it answer?
2. What should the viewer notice first?
3. Can the finding be understood without colour?
4. What text or table alternative could accompany it?
5. Is the scale fair?
6. What important context or limitation remains?
7. What decision can the evidence reasonably support?

You do not need to rebuild the chart in Python.

The aim is to inspect your analytical decisions.

---

## Reflection

This week has shown that responsible visualisation is not a single
formatting choice.

It involves:

- checking that the data structure is correct
- creating a deliberate hierarchy of attention
- using colour as reinforcement rather than the only signal
- providing direct labels and alternative forms of evidence
- representing differences fairly
- adding context that changes interpretation
- evaluating automated outputs
- taking responsibility for the final decision

Tableau and Python can both produce polished charts.

Neither tool can guarantee that a chart is accessible, fair or useful.

That remains the responsibility of the analyst.
