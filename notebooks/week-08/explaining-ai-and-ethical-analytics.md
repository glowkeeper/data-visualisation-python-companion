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

# Week 8 — Behind the Tableau Curtain

## Explaining AI and Ethical Analytics

Week 6 asked whether a claim was **defensible**. Week 7 asked whether an
interaction was **useful**. This week asks a harder question:

> **If a decision-maker acts on this analysis and it turns out to be wrong,
> what could we not have told them?**

Ethics in analysis is rarely a choice between honesty and dishonesty. It is
usually a series of small, reasonable-looking decisions — which measure to
report, which level to aggregate to, which model to fit — each of which quietly
narrows what the audience can see.

This notebook follows one chain:

> **What the data omits → What the measure implies → What the method assumes →
> What must be disclosed**

Python is useful here precisely because it forces the intermediate steps into
the open. A dashboard shows a finished number. Code shows the number *and* the
argument that produced it.

The Python companion is optional and unassessed. No AI account or API key is
required.

---

## Load the retail data

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter
from sklearn.linear_model import LinearRegression

DATASET = "../../data/HighStreetRetailData.xlsx"

df = pd.read_excel(DATASET)
df["Order Date"] = pd.to_datetime(df["Order Date"])

print(f"Rows: {len(df):,}")
df[["Order Date", "Category", "Sub-Category", "Sales", "Discount", "Profit"]].head()
```

A note on colour before we draw anything.

Week 5 established that colour must survive colour-vision deficiency. The
green/orange pairing used in earlier notebooks is comfortable for most readers
but separates poorly under protanopia, so this notebook uses a blue/orange pair
instead — and always pairs colour with a label or a sign, so that no reading
depends on hue alone.

```python
LOSS = "#c55a11"      # orange — negative or at-risk
GAIN = "#3b6ea5"      # blue   — positive
CONTEXT = "#b7b7b7"   # grey   — benchmark, not the subject

MONEY = FuncFormatter(lambda value, _: f"£{value / 1000:,.0f}k")


def tidy(ax, hide=("top", "right")):
    """Recessive axes: keep the data, lose the furniture."""
    ax.spines[list(hide)].set_visible(False)
    ax.set_axisbelow(True)
    return ax
```

---

## Bias begins with what the dataset does not contain

Before questioning a conclusion, inventory the evidence that was available to
produce it.

```python
print(f"Fields: {len(df.columns)}\n")

for field in df.columns:
    print(f"- {field}")
```

The dataset records what the business **sold**. It does not record:

- what the goods cost to buy or hold
- which orders were returned or refunded
- which customers complained, or churned
- what competitors charged that week
- why any particular discount was authorised

This is not a flaw in the file. Every dataset is a boundary drawn by someone,
for some purpose, at some time.

It matters because a boundary is invisible in a dashboard. A chart of Profit by
Category looks complete. Nothing in it announces that returns are missing.

There is a subtler point about `Profit` specifically.

```python
implied_cost = df["Sales"].sum() - df["Profit"].sum()
cost_fields = [c for c in df.columns if "cost" in c.lower()]

print("Can we audit how Profit was calculated?\n")
print(f"Sales                £{df['Sales'].sum():,.0f}")
print(f"Profit               £{df['Profit'].sum():,.0f}")
print(f"Implied total cost   £{implied_cost:,.0f}")
print(f"\nCost fields available to check that against: {cost_fields or 'none'}")
```

The implied cost is arithmetic, not evidence. With no cost field, we cannot say
whether it reflects purchase price, shipping, overhead, or a margin assumption
someone applied before we received the file.

We can reproduce every chart in this module from `Sales` and `Profit`, but we
cannot verify `Profit` itself. We inherited it.

> **Think:** Which of the module's conclusions would change if returns were
> included? Which could not be checked at all?

---

## The measure you choose is an ethical choice

Week 6 compared total Profit across categories. Total Profit is one reasonable
measure. Profit margin is another. They do not agree.

```python
category = (
    df.groupby("Category", as_index=False)
      .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)

category["Margin"] = category["Profit"] / category["Sales"]
category["Sales rank"] = category["Sales"].rank(ascending=False).astype(int)
category["Margin rank"] = category["Margin"].rank(ascending=False).astype(int)

category.sort_values("Sales", ascending=False).style.format(
    {"Sales": "£{:,.0f}", "Profit": "£{:,.0f}", "Margin": "{:.1%}"}
)
```

Look at the two rank columns rather than the money.

```python
# Small multiples must share one category order, otherwise the reader compares
# positions that mean different things in each panel. We order by Sales once and
# keep that order for both, so the margin panel shows the reversal directly.
order = category.sort_values("Sales")
highlight = [LOSS if name == "Furniture" else CONTEXT for name in order["Category"]]

fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

panels = [("Sales", "Total Sales", "£{:,.0f}"), ("Margin", "Profit margin", "{:.1%}")]

for ax, (column, label, fmt) in zip(axes, panels):
    bars = ax.barh(order["Category"], order[column], color=highlight)
    ax.bar_label(
        bars,
        labels=[fmt.format(value) for value in order[column]],
        padding=4,
        fontsize=9,
    )
    ax.set_title(label, loc="left", fontweight="bold")
    ax.set_xlabel("")
    ax.margins(x=0.22)
    ax.get_xaxis().set_visible(False)
    tidy(ax, hide=("top", "right", "bottom"))

fig.suptitle(
    "Same Categories, Same Order — the Ranking Reverses",
    x=0.02,
    ha="left",
    fontweight="bold",
)
plt.tight_layout()
plt.show()
```

Both panels list the categories in the same order, sorted by Sales. Only the
bar lengths change.

Two charts, not one with two axes — the measures are on different scales, and
overlaying them would invent a comparison the data does not support.

Furniture is the **second largest** category by Sales and the **least
profitable** by margin. Office Supplies is the reverse: smallest on Sales,
second on margin.

Both statements are true. A report that includes only one of them is not
inaccurate — it is incomplete in a direction that favours a particular
conclusion.

> **The ethical question is not "is this number correct?" but "does this number
> answer the question the reader thinks it answers?"**

---

## A total can conceal the thing that matters most

Aggregation is the most common way an honest analyst misleads an audience.

The company's overall Profit is positive. That single fact hides a substantial
amount of loss-making trade.

```python
loss_rows = df.loc[df["Profit"] < 0]
gain_rows = df.loc[df["Profit"] >= 0]

summary = pd.DataFrame(
    {
        "Group": ["Profitable lines", "Loss-making lines", "Net position"],
        "Lines": [len(gain_rows), len(loss_rows), len(df)],
        "Sales": [gain_rows["Sales"].sum(), loss_rows["Sales"].sum(), df["Sales"].sum()],
        "Profit": [
            gain_rows["Profit"].sum(),
            loss_rows["Profit"].sum(),
            df["Profit"].sum(),
        ],
    }
)

summary.style.format({"Lines": "{:,}", "Sales": "£{:,.0f}", "Profit": "£{:,.0f}"})
```

```python
share_of_lines = len(loss_rows) / len(df)
share_of_sales = loss_rows["Sales"].sum() / df["Sales"].sum()

print(f"Loss-making lines:      {share_of_lines:.1%} of all order lines")
print(f"Sales on those lines:   {share_of_sales:.1%} of total Sales")
print(f"Loss carried by them:   £{loss_rows['Profit'].sum():,.0f}")
print(f"Reported net Profit:    £{df['Profit'].sum():,.0f}")
```

```python
fig, ax = plt.subplots(figsize=(9, 3.6))

plot = summary.iloc[[0, 1, 2]]
colours = [GAIN, LOSS, CONTEXT]

bars = ax.barh(plot["Group"], plot["Profit"], color=colours)
ax.bar_label(
    bars,
    labels=[f"£{value / 1000:,.0f}k" for value in plot["Profit"]],
    padding=5,
    fontsize=9,
)
ax.axvline(0, color="#555555", linewidth=1)
ax.set_title(
    "The Net Figure Is What Remains After a Large Offset",
    loc="left",
    fontweight="bold",
)
ax.xaxis.set_major_formatter(MONEY)
ax.set_xlabel("Profit")
ax.margins(x=0.16)
ax.grid(axis="x", alpha=0.2)
tidy(ax, hide=("top", "right", "left"))

plt.tight_layout()
plt.show()
```

Roughly a fifth of all order lines lose money, and they carry roughly a fifth
of all Sales. The reported net figure is the residue left after those losses
are absorbed by profitable trade.

A dashboard tile reading **Total Profit £292k** is arithmetically correct and
tells the reader almost nothing about the business's actual condition.

> **Think:** Would a manager act differently if the tile also showed the value
> of loss-making trade? Which decision does each version support?

---

## Where the losses are concentrated

We have a `Discount` field, so one explanation is directly testable.

```python
bands = pd.cut(
    df["Discount"],
    bins=[-0.001, 0, 0.10, 0.20, 0.30, 0.50, 1.0],
    labels=["0%", "1–10%", "11–20%", "21–30%", "31–50%", "over 50%"],
)

discount = (
    df.groupby(bands, observed=False)
      .agg(Lines=("Row ID", "count"), Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)

discount["Margin"] = discount["Profit"] / discount["Sales"]
discount.style.format(
    {"Lines": "{:,}", "Sales": "£{:,.0f}", "Profit": "£{:,.0f}", "Margin": "{:.1%}"}
)
```

```python
fig, ax = plt.subplots(figsize=(9, 4.4))

plot = discount.reset_index()
colours = [LOSS if value < 0 else GAIN for value in plot["Margin"]]

bars = ax.bar(plot["Discount"].astype(str), plot["Margin"], color=colours)
ax.bar_label(
    bars,
    labels=[f"{value:.0%}" for value in plot["Margin"]],
    padding=4,
    fontsize=9,
)
ax.axhline(0, color="#555555", linewidth=1)
ax.set_title(
    "Margin Turns Negative Above a 20% Discount",
    loc="left",
    fontweight="bold",
)
ax.set_xlabel("Discount band")
ax.set_ylabel("Profit margin")
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0%}"))
ax.grid(axis="y", alpha=0.2)
tidy(ax)

plt.tight_layout()
plt.show()
```

The pattern is sharp. Bands up to 20% are profitable; every band above it is
not.

It is very tempting to convert this into a rule:

> *Cap all discounts at 20%.*

Pause before doing so. That sentence is no longer an observation about a
dataset — it is a policy that would change what sales staff may offer, which
customers get a deal, and which accounts become uncompetitive.

The evidence supports an **association**. The policy assumes a **cause**, and
assumes that the relationship would survive the intervention. Deep discounts
may be a *symptom* of hard-to-sell stock rather than the reason it loses money.

```python
deep = df.loc[df["Discount"] > 0.20]

print("What sits behind the deep-discount lines?\n")
print(
    deep.groupby("Category")
        .agg(Lines=("Row ID", "count"), Profit=("Profit", "sum"))
        .sort_values("Profit")
        .to_string()
)
print("\nThe dataset cannot tell us why those discounts were authorised.")
```

> **Analysis describes what happened. A policy decides what happens next to
> people. The second needs more evidence than the first.**

---

## A forecast is an argument, not a fact

Tableau will draw a forecast line through a time series without ever showing
the reasoning. Let us fit the equivalent model in Python and then insist that
it explain itself.

```python
monthly = (
    df.assign(Month=df["Order Date"].dt.to_period("M").dt.to_timestamp())
      .groupby("Month", as_index=False)
      .agg(Sales=("Sales", "sum"))
      .sort_values("Month")
      .reset_index(drop=True)
)

monthly["Month number"] = np.arange(len(monthly))

model = LinearRegression().fit(monthly[["Month number"]], monthly["Sales"])
monthly["Trend"] = model.predict(monthly[["Month number"]])
residuals = monthly["Sales"] - monthly["Trend"]

next_month = pd.DataFrame({"Month number": [len(monthly)]})
point_forecast = model.predict(next_month)[0]
residual_sd = residuals.std(ddof=2)

print(f"Months of history:   {len(monthly)}")
print(f"Trend:               £{model.coef_[0]:,.0f} per month")
print(f"R-squared:           {model.score(monthly[['Month number']], monthly['Sales']):.3f}")
print(f"Residual std dev:    £{residual_sd:,.0f}")
print(f"\nPoint forecast:      £{point_forecast:,.0f}")
print(
    f"95% interval:        £{point_forecast - 1.96 * residual_sd:,.0f} "
    f"to £{point_forecast + 1.96 * residual_sd:,.0f}"
)
```

Now plot the number *with* its uncertainty, which is the part a dashboard tile
usually discards.

```python
fig, ax = plt.subplots(figsize=(10, 4.6))

ax.plot(monthly["Month"], monthly["Sales"], color=CONTEXT, linewidth=1.6, label="Actual")
ax.plot(monthly["Month"], monthly["Trend"], color=GAIN, linewidth=2, label="Fitted trend")

future_month = monthly["Month"].iloc[-1] + pd.DateOffset(months=1)
ax.errorbar(
    future_month,
    point_forecast,
    yerr=1.96 * residual_sd,
    fmt="o",
    color=LOSS,
    markersize=8,
    capsize=6,
    linewidth=2,
    label="Forecast (95% interval)",
)

ax.set_title(
    "The Forecast Point Is Confident. The Interval Is Not.",
    loc="left",
    fontweight="bold",
)
ax.yaxis.set_major_formatter(MONEY)
ax.set_ylabel("Monthly Sales")
ax.set_xlabel("")
ax.grid(axis="y", alpha=0.2)
ax.legend(frameon=False, loc="upper left")
tidy(ax)

plt.tight_layout()
plt.show()
```

```python
interval_width = 2 * 1.96 * residual_sd

print(f"Interval width: £{interval_width:,.0f}")
print(f"As a share of the forecast: {interval_width / point_forecast:.0%}")
```

The 95% interval is wider than the forecast it surrounds.

That is not a broken model. It is an honest one, reporting that monthly Sales
in this dataset are mostly *not* explained by a straight line.

---

### A real trend and a worthless prediction

The trend is genuine *and* the next-month forecast is nearly useless. Both are
true at the same time, and holding them together is the whole lesson.

First, check whether the trend itself is more than noise.

```python
month_numbers = monthly["Month number"]
spread_of_x = ((month_numbers - month_numbers.mean()) ** 2).sum()

slope_standard_error = residual_sd / np.sqrt(spread_of_x)
t_statistic = model.coef_[0] / slope_standard_error

print(f"Slope                £{model.coef_[0]:,.0f} per month")
print(f"Standard error       £{slope_standard_error:,.0f}")
print(f"t statistic          {t_statistic:.2f}")
print(
    "\nA t statistic near 4 means the upward trend is very unlikely "
    "to be an accident of sampling."
)
```

So the trend is genuine. Now look at what it does for a single month.

```python
print(f"Spread of monthly Sales, ignoring the trend:  £{monthly['Sales'].std(ddof=1):,.0f}")
print(f"Spread still left after fitting the trend:    £{residual_sd:,.0f}")
```

Knowing the trend barely narrows the uncertainty about any given month. The
line describes four years well and predicts next month badly, because the
month-to-month noise is far larger than the monthly drift.

This is the trap:

> **"Statistically significant" licenses a claim about the pattern. It does not
> license a confident claim about the next value.**

A student who reports only the £911 per month trend is telling the truth. A
student who then presents the point forecast as a plan is not.

### Our interval is itself an understatement

Honesty applies to our own method too. The band above uses a shortcut: 1.96
times the spread of the residuals. It ignores that the fitted line is itself
uncertain, and that we are predicting beyond the end of the data.

```python
leverage = 1 + 1 / len(monthly) + (
    (len(monthly) - month_numbers.mean()) ** 2 / spread_of_x
)
proper_error = residual_sd * np.sqrt(leverage)
t_critical = 2.013  # 97.5th percentile, 46 degrees of freedom

print(f"Simple band   ±£{1.96 * residual_sd:,.0f}   ({2 * 1.96 * residual_sd / point_forecast:.0%} of the forecast)")
print(f"Proper band   ±£{t_critical * proper_error:,.0f}   ({2 * t_critical * proper_error / point_forecast:.0%} of the forecast)")
```

The properly calculated interval is wider still. Our shortcut errs towards
*overconfidence*, which is the direction that matters — so the notebook states
it rather than quietly benefiting from it.

One reassurance that the band is not theatrical:

```python
inside = (residuals.abs() <= 1.96 * residual_sd).mean()
print(f"{inside:.0%} of historical months fall inside ±1.96 × residual spread")
```

Close to the nominal 95%. The uncertainty is real, not manufactured to make a
point.

The danger is that the point forecast survives into a slide deck and the
interval does not.

```python
opaque = f"Sales next month: £{point_forecast:,.0f}."

transparent = (
    f"Sales next month are estimated at £{point_forecast:,.0f}, based on a linear "
    f"trend fitted to {len(monthly)} months of history. The model explains "
    f"{model.score(monthly[['Month number']], monthly['Sales']):.0%} of past variation, "
    f"so the realistic range is roughly £{point_forecast - 1.96 * residual_sd:,.0f} "
    f"to £{point_forecast + 1.96 * residual_sd:,.0f}. It assumes no change in "
    "pricing, promotion or store count, and excludes returns."
)

print("OPAQUE\n" + opaque)
print("\nTRANSPARENT\n" + transparent)
```

Both sentences describe the same model. Only the second can be challenged —
and only a claim that can be challenged can be trusted.

---

## Write the analysis card

For Assessment 2 you must evaluate and justify an analytical capability. That
is much easier if you record the five things a reader needs in order to
interrogate it.

```python
analysis_card = pd.Series(
    {
        "What data it used": (
            f"{len(monthly)} months of aggregated Sales, "
            f"{monthly['Month'].min():%b %Y} to {monthly['Month'].max():%b %Y}"
        ),
        "What method produced it": "Ordinary least squares linear trend on month number",
        "What it assumes": (
            "The trend continues; no seasonality; no change in pricing, "
            "promotion or store count"
        ),
        "What it cannot tell you": (
            "Why Sales move; the effect of returns, cost or competitor action"
        ),
        "How confident, and why": (
            f"Low. R-squared {model.score(monthly[['Month number']], monthly['Sales']):.2f}; "
            f"95% interval ±£{1.96 * residual_sd:,.0f}"
        ),
    },
    name="Monthly Sales trend forecast",
)

analysis_card.to_frame()
```

Write one of these for every automated or AI-assisted element in your project.
If a row cannot be completed, that gap **is** the finding — report it rather
than hiding it.

---

## Apply the ethics checklist

The Week 8 lecture ends with a checklist. Some of it can be checked mechanically.

```python
claim = "Furniture is our strongest category."

checks = pd.DataFrame(
    {
        "Check": [
            "The title matches the evidence",
            "The measure answers the question asked",
            "What is missing is stated, not hidden",
            "Uncertainty is visible",
            "Any AI contribution has been evaluated",
            "You can explain how the result was produced",
        ],
        "Verdict": [
            "No — strongest on Sales rank, weakest on margin",
            "No — 'strongest' implies profitability, Sales was used",
            "No — returns and product cost are absent and unstated",
            "No — a single total implies precision it does not have",
            "Not applicable here; required if AI wrote any of it",
            "Yes — the aggregation is reproducible from this notebook",
        ],
    }
)

print(f"Claim under review: {claim}\n")
checks
```

Five of six fail. The claim is not a lie — Furniture really does out-sell
Office Supplies. It fails because the words carry an implication the evidence
does not support.

```python
revised_claim = (
    "Furniture generates the second-highest Sales but the lowest profit margin "
    "of the three categories in this dataset. Returns and product cost are not "
    "included, so profitability may be overstated."
)

print(revised_claim)
print(f"\nWord count: {len(revised_claim.split())}")
```

Longer, duller, defensible.

---

## Responsibility does not transfer to the tool

Suppose a recommendation built on this analysis turns out badly.

```python
accountability = pd.DataFrame(
    {
        "Participant": [
            "The dataset",
            "The forecasting model",
            "An AI assistant",
            "The dashboard",
            "The analyst",
        ],
        "What it contributed": [
            "A boundary around what could be measured",
            "An extrapolation with a stated interval",
            "Fluent text and plausible explanations",
            "A selection of what the reader sees first",
            "Every choice above, and the framing of the result",
        ],
        "Can it be held accountable?": [
            "No",
            "No",
            "No",
            "No",
            "Yes",
        ],
    }
)

accountability
```

Each component narrowed what the decision-maker could see. Only one of them can
answer for that in a meeting.

> **AI suggests. The analyst evaluates. The analyst decides — and the analyst
> answers for the decision.**

---

## Your turn — audit your own analysis

Take one claim from your Tableau dashboard, ideally the one you intend to put
in front of the Assessment 2 board.

```python
my_audit = {
    "The claim I want to make": "",
    "The measure it actually uses": "",
    "A different measure that would change it": "",
    "What the dataset cannot show": "",
    "How uncertain the result is, and why": "",
    "How I would state the limitation to the board": "",
}

pd.Series(my_audit, name="My ethical audit").to_frame()
```

Then:

1. Rewrite the claim so the wording matches the evidence exactly.
2. Complete an analysis card for any forecast, trend or AI-assisted element.
3. Name one decision the claim could wrongly influence.
4. Decide what you would disclose before anyone acts on it.

If you use AI, ask it to challenge your audit rather than to write it:

> *I have a retail dashboard showing Sales and Profit by category. What might my
> analysis be hiding, and what evidence would test it?*

Then evaluate each challenge against the dataset. A fluent criticism is still
only a suggestion.

---

## What Python revealed

Tableau made the pattern visible. Python exposed the decisions that produced it:

- the field list defined a boundary that no chart displays
- `Profit` was inherited, not derived, and cannot be audited here
- the choice between total and margin reversed a category ranking
- a positive net figure concealed a fifth of trade losing money
- a sharp discount pattern was an association, not a licence to set policy
- a confident forecast carried an interval wider than itself
- an analysis card turned "trust me" into something checkable
- accountability stayed with a person at every step

The lesson is not that dashboards are dishonest. It is that every summary is a
compression, and compression discards whatever the author did not think to
keep.

> **An ethical analysis is not one that avoids uncertainty. It is one that
> leaves the reader able to find it.**
