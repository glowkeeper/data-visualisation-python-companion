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

# Week 7 — Behind the Tableau Curtain

## Interactive Visualisations with Plotly

In Tableau, adding a filter can feel like a design operation: drag a field,
show the control and test the dashboard.

Python makes us state more of the reasoning explicitly:

- which values the user can select
- which marks should change
- which context should remain visible
- what question the interaction answers

This notebook is not a separate programming lesson. It explores the analytical
idea behind the Week 7 Tableau workshop:

> **Every interaction should help an intended user answer a useful question.**

We will follow one chain:

> **User → Question → Interaction → Evidence → Decision**

The Python companion is optional and unassessed. Its purpose is to reveal some
of the choices that dashboard software handles behind the curtain.

---

## Load the retail data

```python
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def find_dataset():
    """Find the shared dataset from either the repository or notebook folder."""
    candidates = [
        Path("data/HighStreetRetailData.xlsx"),
        Path("../../data/HighStreetRetailData.xlsx"),
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError("Could not find data/HighStreetRetailData.xlsx")


DATASET = find_dataset()
df = pd.read_excel(DATASET)
df["Order Date"] = pd.to_datetime(df["Order Date"])

print(f"Loaded {len(df):,} rows from {DATASET}")
df[["Order Date", "Category", "Sales", "Profit"]].head()
```

Before building a control, check the values it will expose.

```python
categories = sorted(df["Category"].dropna().unique())
date_range = (df["Order Date"].min(), df["Order Date"].max())

print("Categories:")
for category in categories:
    print(f"- {category}")

print(
    f"\nDate range: {date_range[0]:%d %B %Y} "
    f"to {date_range[1]:%d %B %Y}"
)
```

The three Category values and the available date range define the valid choices
for our first interactions.

---

## Begin with a fixed comparison

A static chart offers one prepared view. It can answer a useful question when
the author has chosen that question in advance.

Here the question is:

> **How do total Sales and Profit compare across categories?**

```python
category_totals = (
    df.groupby("Category", as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Profit=("Profit", "sum"),
      )
      .sort_values("Sales", ascending=False)
      .reset_index(drop=True)
)

category_totals.style.format({"Sales": "£{:,.0f}", "Profit": "£{:,.0f}"})
```

```python
fixed_figure = px.bar(
    category_totals,
    x="Category",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales and Profit Tell Different Category Stories",
    labels={"value": "Amount (£)", "variable": "Measure"},
    color_discrete_map={"Sales": "#3b6ea5", "Profit": "#c55a11"},
)

fixed_figure.update_layout(
    hovermode="x unified",
    legend_title_text="",
    yaxis_tickprefix="£",
    yaxis_tickformat=",.0f",
)
fixed_figure.show()
```

Furniture produces slightly more Sales than Office Supplies, but substantially
less Profit. The fixed comparison makes that mismatch visible.

It does not let a user investigate when the mismatch occurred.

> **Think:** What useful follow-up question does the fixed view create?

---

## Interaction 1 — a category control

We will now let the user ask:

> **How did Sales and Profit change over time for a selected category?**

First, prepare monthly evidence. This aggregation is another decision: daily
data would be more detailed, but much noisier.

```python
monthly_category = (
    df.assign(Month=df["Order Date"].dt.to_period("M").dt.to_timestamp())
      .groupby(["Month", "Category"], as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Profit=("Profit", "sum"),
      )
      .sort_values(["Category", "Month"])
)

monthly_category.head()
```

Plotly dropdown buttons work by changing which prepared traces are visible.
The code is longer than the equivalent Tableau action because the interaction
logic is explicit.

```python
category_figure = go.Figure()

for category_index, category in enumerate(categories):
    category_data = monthly_category.loc[
        monthly_category["Category"].eq(category)
    ]

    category_figure.add_trace(
        go.Scatter(
            x=category_data["Month"],
            y=category_data["Sales"],
            name="Sales",
            line={"color": "#3b6ea5", "width": 2.5},
            visible=category_index == 0,
            hovertemplate="%{x|%b %Y}<br>Sales: £%{y:,.0f}<extra></extra>",
        )
    )
    category_figure.add_trace(
        go.Scatter(
            x=category_data["Month"],
            y=category_data["Profit"],
            name="Profit",
            line={"color": "#c55a11", "width": 2.5},
            visible=category_index == 0,
            hovertemplate="%{x|%b %Y}<br>Profit: £%{y:,.0f}<extra></extra>",
        )
    )

buttons = []

for category_index, category in enumerate(categories):
    visible = [False] * (len(categories) * 2)
    visible[category_index * 2] = True
    visible[category_index * 2 + 1] = True

    buttons.append(
        {
            "label": category,
            "method": "update",
            "args": [
                {"visible": visible},
                {"title": f"Monthly Sales and Profit — {category}"},
            ],
        }
    )

category_figure.update_layout(
    title=f"Monthly Sales and Profit — {categories[0]}",
    xaxis_title="",
    yaxis_title="Amount (£)",
    yaxis_tickprefix="£",
    yaxis_tickformat=",.0f",
    hovermode="x unified",
    legend_title_text="",
    updatemenus=[
        {
            "buttons": buttons,
            "direction": "down",
            "showactive": True,
            "x": 1,
            "xanchor": "right",
            "y": 1.18,
            "yanchor": "top",
        }
    ],
    annotations=[
        {
            "text": "Choose a category:",
            "x": 0.74,
            "xref": "paper",
            "y": 1.145,
            "yref": "paper",
            "showarrow": False,
        }
    ],
)
category_figure.show()
```

Use the dropdown to compare Furniture, Office Supplies and Technology.

Do not ask only, “Did the chart change?” Ask:

- What question did the selection answer?
- What pattern became clearer?
- What comparison became harder?
- What remains uncertain?

---

## Interaction can remove context

Filtering creates focus by removing marks. That can help—but it can also make a
selected value look important simply because nothing else remains.

For a decision about Furniture, retaining the category benchmark may be more
useful than showing Furniture alone.

```python
comparison = category_totals.copy()
comparison["Profit margin"] = comparison["Profit"] / comparison["Sales"]
comparison["Focus"] = comparison["Category"].map(
    lambda value: "Furniture" if value == "Furniture" else "Other categories"
)

context_figure = px.bar(
    comparison.sort_values("Profit margin"),
    x="Profit margin",
    y="Category",
    orientation="h",
    color="Focus",
    text="Profit margin",
    title="Furniture's Profit Margin Is Weakest in the Category Context",
    color_discrete_map={
        "Furniture": "#c55a11",
        "Other categories": "#b7b7b7",
    },
)

context_figure.update_traces(
    texttemplate="%{text:.1%}",
    textposition="outside",
    hovertemplate="%{y}<br>Profit margin: %{x:.1%}<extra></extra>",
)
context_figure.update_layout(
    xaxis_title="Profit margin",
    xaxis_tickformat=".0%",
    yaxis_title="",
    legend_title_text="",
    showlegend=False,
)
context_figure.show()
```

The highlight creates focus; the other categories preserve the benchmark.

> **Think:** When should a filter remove context? When should highlighting keep
> the comparison visible?

---

## Interaction 2 — inspect a mismatch

The category view suggests that high Sales do not guarantee high Profit. A
scatter plot lets the user inspect the relationship at Sub-Category level.

The analytical question is:

> **Which Sub-Categories combine substantial Sales with weak or negative
> Profit?**

```python
subcategory_performance = (
    df.groupby(["Category", "Sub-Category"], as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Profit=("Profit", "sum"),
          Orders=("Order ID", "nunique"),
      )
)

mismatch_figure = px.scatter(
    subcategory_performance,
    x="Sales",
    y="Profit",
    color="Category",
    size="Orders",
    hover_name="Sub-Category",
    custom_data=["Category", "Orders"],
    title="Sub-Categories Reveal Where Sales and Profit Diverge",
    color_discrete_map={
        "Furniture": "#c55a11",
        "Office Supplies": "#cc79a7",
        "Technology": "#3b6ea5",
    },
)

mismatch_figure.add_hline(y=0, line_color="#555555", line_width=1)
mismatch_figure.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "Category: %{customdata[0]}<br>"
        "Sales: £%{x:,.0f}<br>"
        "Profit: £%{y:,.0f}<br>"
        "Orders: %{customdata[1]:,.0f}<extra></extra>"
    )
)
mismatch_figure.update_layout(
    xaxis_title="Sales (£)",
    yaxis_title="Profit (£)",
    xaxis_tickprefix="£",
    yaxis_tickprefix="£",
    legend_title_text="Category",
)
mismatch_figure.show()
```

Try these interactions:

1. Hover over points to inspect their exact evidence.
2. Click a Category in the legend to hide it.
3. Double-click a Category in the legend to isolate it.
4. Drag across an area to zoom, then double-click the plot to reset.

Each interaction supports a different question. Hiding a category is not
automatically useful; it is useful only when that narrower view helps the user
investigate something relevant.

The chart can locate a mismatch. It cannot establish its cause.

---

## Evaluate the interaction, not just the chart

A working control is only a technical success. An effective control must also
help the intended user reason.

```python
interaction_audit = pd.DataFrame(
    {
        "Interaction": [
            "Category dropdown",
            "Hover details",
            "Legend selection",
            "Zoom",
        ],
        "Question it can answer": [
            "How do Sales and Profit change over time for this category?",
            "What exact evidence belongs to this mark?",
            "How does one category compare with or without the others?",
            "What happens in this narrower range?",
        ],
        "Possible risk": [
            "Filtering removes the category benchmark",
            "Important evidence is hidden until discovered",
            "The user may forget that categories were hidden",
            "The user may lose the full time or value context",
        ],
        "Useful design response": [
            "Keep the current selection visible in the title",
            "Put essential evidence in labels or nearby text",
            "Make the active legend state clear",
            "Provide an obvious reset route",
        ],
    }
)

interaction_audit
```

This audit reveals a trade-off:

> **Interaction increases choice, but also increases the user's responsibility
> to understand the current state.**

---

## Interactive, automated and AI-assisted are different

These terms are related, but they are not interchangeable.

```python
system_types = pd.DataFrame(
    {
        "Capability": [
            "Category dropdown",
            "Scheduled data refresh",
            "Rule-based profit alert",
            "Statistical anomaly flag",
            "AI-generated explanation",
        ],
        "Primary type": [
            "Interaction",
            "Automation",
            "Automation",
            "Statistical analytics",
            "AI-assisted interpretation",
        ],
        "What the analyst must evaluate": [
            "Whether the control answers a useful question",
            "Whether the source, timing and status are trustworthy",
            "Whether the threshold is meaningful",
            "Whether the method and false positives are acceptable",
            "Whether the explanation is supported by evidence",
        ],
    }
)

system_types
```

A dashboard is not AI-enabled merely because it refreshes automatically or
applies a rule. Whatever the capability, the analyst remains responsible for
its relevance, evidence and limitations.

---

## Assessment 2 checkpoint

For Assessment 2, the number of controls is less important than the analytical
value they provide.

Use the following cell as a project-planning prompt. Replace the example text
with your own intended user, decision and interaction.

```python
intended_user = "Retail category manager"
decision = "Where should we investigate weak profitability first?"
interaction = "Select a category, then inspect its Sub-Categories"
interaction_question = "Where is weak category Profit concentrated?"

assessment_checkpoint = pd.DataFrame(
    {
        "Design question": [
            "Who is the intended user?",
            "What decision do they need to make?",
            "What interaction helps them?",
            "What question does that interaction answer?",
        ],
        "Current answer": [
            intended_user,
            decision,
            interaction,
            interaction_question,
        ],
    }
)

assessment_checkpoint
```

Now challenge the design:

- What context could the interaction hide?
- How will the user know which state is active?
- How can the user reset the view?
- What evidence supports the resulting decision?
- What remains uncertain?

---

## Final reflection

This notebook used Plotly to reproduce ideas that Tableau expresses through
filters, actions, tooltips and interactive marks.

The important lesson is not the Python syntax.

It is that every interaction contains an argument about:

- who the user is
- what they need to ask
- what should change
- what context should remain
- what decision the evidence can support

The code makes those choices visible, but it does not make them for us.

> **A good interactive dashboard does not merely respond to clicks. It helps an
> intended user ask a useful question without losing the evidence needed to
> interpret the answer.**
