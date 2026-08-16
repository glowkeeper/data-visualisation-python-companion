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

# Week 6 — Behind the Tableau Curtain

## AI-Assisted Data Analysis

This week moves from a clear insight to a **defensible decision**.

Tableau can show a pattern. Python can test that pattern at another level
of detail. An AI assistant can suggest explanations or challenge a
recommendation.

None of them can remove the analyst's responsibility for the reasoning.

This notebook follows one chain:

> **Evidence → Claim → Explanation → Options → Decision**

At every step, we will ask what the evidence supports, what has been
inferred and what remains unknown.

No AI account or API key is required. The notebook uses example
AI-style responses so that everyone can audit the same claims.

---

## A fluent answer is not evidence

An AI assistant can quickly produce:

- a confident explanation
- a list of possible causes
- a polished recommendation
- a challenge to our reasoning

That can be useful for generating questions. It is not the same as
answering those questions with data.

The distinction for this week is:

> **Use AI to widen the investigation, not to certify the conclusion.**

---

## Load the retail data

```python
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

DATASET = "../../data/HighStreetRetailData.xlsx"

df = pd.read_excel(DATASET)

df[["Category", "Sub-Category", "Sales", "Discount", "Profit"]].head()
```

---

## Check what evidence is actually available

Before asking why something happened, inspect the fields we have.

```python
available_fields = df.columns.tolist()

print(f"Rows: {len(df):,}")
print(f"Fields: {len(available_fields)}")
print("\nAvailable fields:")

for field in available_fields:
    print(f"- {field}")
```

The dataset includes Sales, Profit, Quantity and Discount. It does not
include:

- supplier cost
- competitor price
- customer satisfaction
- product returns
- marketing activity

This boundary matters. An explanation involving a missing field may be
plausible, but this dataset cannot test it directly.

> **Think:** Which business questions can these fields answer? Which can
> they only suggest?

---

## Evidence: what does the category view show?

We will reproduce the dashboard's category totals.

```python
category_evidence = (
    df.groupby("Category", as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Profit=("Profit", "sum"),
      )
      .sort_values("Profit")
      .reset_index(drop=True)
)

category_evidence
```

```python
fig, ax = plt.subplots(figsize=(9, 4.5))

colours = [
    "#c55a11" if category == "Furniture" else "#b7b7b7"
    for category in category_evidence["Category"]
]

bars = ax.barh(
    category_evidence["Category"],
    category_evidence["Profit"],
    color=colours,
)

ax.bar_label(
    bars,
    labels=[f"£{value / 1000:,.0f}k" for value in category_evidence["Profit"]],
    padding=5,
)
ax.set_title("Furniture Generates the Lowest Total Profit", loc="left", fontweight="bold")
ax.set_xlabel("Profit")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"£{value / 1000:,.0f}k"))
ax.spines[["top", "right", "left"]].set_visible(False)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
```

The chart supports this observation:

> **Furniture has the lowest total Profit of the three categories in
> this dataset.**

It does not establish why.

---

## Separate observation from inference

Consider three statements:

1. Furniture has the lowest total Profit.
2. Furniture's product mix may contribute to its low Profit.
3. Supplier costs caused Furniture's low Profit.

```python
claim_audit = pd.DataFrame(
    {
        "Statement": [
            "Furniture has the lowest total Profit.",
            "Furniture's product mix may contribute to its low Profit.",
            "Supplier costs caused Furniture's low Profit.",
        ],
        "Type": [
            "Observation",
            "Inference",
            "Causal claim",
        ],
        "Status": [
            "Supported",
            "Requires a focused test",
            "Not testable with available fields",
        ],
    }
)

claim_audit
```

The wording changes the strength of the claim:

- **has** reports a measured comparison
- **may contribute** proposes an explanation to investigate
- **caused** asserts a relationship that needs stronger evidence

Qualification is not weakness. It makes the boundary of the evidence
visible.

---

## An AI-style explanation

Imagine an assistant receives only the category chart and responds:

> Furniture is less profitable because supplier costs and discounting
> are too high. The company should discontinue its Furniture range.

The answer sounds decisive. Let us audit it sentence by sentence.

```python
ai_claims = pd.DataFrame(
    {
        "AI statement": [
            "Furniture is less profitable than the other categories.",
            "Supplier costs are too high.",
            "Discounting is too high.",
            "The company should discontinue Furniture.",
        ],
        "Evidence status": [
            "Supported by category totals",
            "Not shown: supplier cost is absent",
            "Testable association; not yet a cause",
            "Decision exceeds the current evidence",
        ],
        "Next step": [
            "Report the comparison precisely",
            "Obtain cost data",
            "Compare Discount and Profit at a finer level",
            "Compare lower-risk and reversible options",
        ],
    }
)

ai_claims
```

Notice that we did not label the whole response "right" or "wrong".
We separated:

- a supported observation
- an untestable explanation
- a testable possibility
- an unsupported decision

This is more useful than accepting or rejecting AI as a single block.

---

## Challenge the first explanation

One possible explanation is **product mix**: perhaps Furniture's weak
result is concentrated in particular Sub-Categories.

Python can perform the same focused diagnostic view as the Week 6
Tableau workshop.

```python
furniture_evidence = (
    df.loc[df["Category"].eq("Furniture")]
      .groupby("Sub-Category", as_index=False)
      .agg(
          Sales=("Sales", "sum"),
          Profit=("Profit", "sum"),
          Average_Discount=("Discount", "mean"),
          Orders=("Order ID", "nunique"),
      )
      .sort_values("Profit")
      .reset_index(drop=True)
)

furniture_evidence
```

```python
fig, ax = plt.subplots(figsize=(9, 5))

colours = [
    "#c55a11" if value < 0 else "#3b6ea5"
    for value in furniture_evidence["Profit"]
]

bars = ax.barh(
    furniture_evidence["Sub-Category"],
    furniture_evidence["Profit"],
    color=colours,
)

ax.axvline(0, color="#555555", linewidth=1)
ax.bar_label(
    bars,
    labels=[f"£{value / 1000:,.1f}k" for value in furniture_evidence["Profit"]],
    padding=4,
)
ax.set_title("Furniture Profit Is Not Evenly Distributed", loc="left", fontweight="bold")
ax.set_xlabel("Profit")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"£{value / 1000:,.0f}k"))
ax.margins(x=0.14)  # room for the outside label on the longest negative bar
ax.spines[["top", "right", "left"]].set_visible(False)
ax.grid(axis="x", alpha=0.2)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
```

The category total hides substantial variation:

- Chairs and Furnishings generate positive Profit
- Tables and Bookcases generate negative Profit

This evidence supports a narrower observation: weak Furniture Profit is
concentrated in some Sub-Categories.

It does **not** prove that product mix caused the category result. The
mix describes where the result occurs; we still need to investigate why.

---

## Test a second possibility: discounting

The dataset contains Discount, so we can ask whether higher discounts
are associated with lower Profit in Furniture orders.

We will create discount bands to make the comparison visible.

```python
furniture_orders = df.loc[df["Category"].eq("Furniture")].copy()

furniture_orders["Discount band"] = pd.cut(
    furniture_orders["Discount"],
    bins=[-0.001, 0, 0.2, 0.4, 1.0],
    labels=["No discount", "Up to 20%", "21–40%", "Over 40%"],
)

discount_evidence = (
    furniture_orders.groupby("Discount band", observed=False)
      .agg(
          Rows=("Row ID", "count"),
          Sales=("Sales", "sum"),
          Profit=("Profit", "sum"),
          Average_Profit=("Profit", "mean"),
      )
)

discount_evidence
```

```python
fig, ax = plt.subplots(figsize=(9, 4.5))

plot_data = discount_evidence.reset_index()
colours = ["#c55a11" if value < 0 else "#3b6ea5" for value in plot_data["Profit"]]

bars = ax.bar(
    plot_data["Discount band"].astype(str),
    plot_data["Profit"],
    color=colours,
)

ax.axhline(0, color="#555555", linewidth=1)
ax.bar_label(
    bars,
    labels=[f"£{value / 1000:,.1f}k" for value in plot_data["Profit"]],
    padding=4,
)
ax.set_title("Furniture Profit by Discount Band", loc="left", fontweight="bold")
ax.set_xlabel("Discount band")
ax.set_ylabel("Profit")
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"£{value / 1000:,.0f}k"))
ax.margins(y=0.16)  # keep the negative labels clear of the axis ticks
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.2)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()
```

If high-discount bands have lower Profit, we have found an association
worth investigating.

We have not proved causation. Discount may interact with:

- Sub-Category
- product price and cost
- order quantity
- region or customer segment
- the reason the discount was offered

> **Think:** What comparison would you run next? What missing field
> would most improve the test?

---

## Build an evidence register

An evidence register prevents a polished narrative from concealing gaps.

```python
evidence_register = pd.DataFrame(
    {
        "Reasoning step": [
            "Observation",
            "Finer-level pattern",
            "Possible explanation",
            "Missing evidence",
        ],
        "Current statement": [
            "Furniture has the lowest total category Profit.",
            "Losses are concentrated in Tables and Bookcases.",
            "Discounting may contribute to weak Profit.",
            "Product cost and returns are not available.",
        ],
        "Strength": [
            "Directly supported",
            "Directly supported",
            "Association to investigate",
            "Known limitation",
        ],
    }
)

evidence_register
```

The register keeps observations, explanations and limitations in
different rows. That separation makes overclaiming easier to detect.

---

## One insight does not dictate one action

Suppose a decision-maker asks what the company should do next.

We can compare three responses:

```python
options = pd.DataFrame(
    {
        "Option": [
            "Discontinue Furniture immediately",
            "Run a targeted test in Tables and Bookcases",
            "Analyse discount, cost and returns before acting",
        ],
        "Potential benefit": ["High", "Moderate", "Moderate"],
        "Risk": ["High", "Low", "Low"],
        "Speed": ["Fast", "Moderate", "Slow"],
        "Reversibility": ["Low", "High", "High"],
        "Fit with current evidence": ["Weak", "Strong", "Strong"],
    }
)

options
```

This is not an automatic decision model. The words in the table are
judgements that should be debated.

Its purpose is to stop the largest action from appearing to be the only
action.

With incomplete causal evidence, a limited and reversible test is more
proportionate than a category-wide commitment.

---

## Write a qualified recommendation

A defensible recommendation shows its working.

```python
lowest_subcategories = furniture_evidence.loc[
    furniture_evidence["Profit"].lt(0),
    "Sub-Category",
].tolist()

recommendation = (
    f"We recommend a limited test focused on {' and '.join(lowest_subcategories)} "
    "because Furniture has the lowest category Profit and losses are concentrated "
    "in those Sub-Categories. However, this analysis cannot establish the cause. "
    "The next step should compare discount, product cost, volume and returns before "
    "any category-wide decision."
)

print(recommendation)
print(f"\nWord count: {len(recommendation.split())}")
```

The recommendation contains four visible parts:

- **action** — run a limited test
- **evidence** — low category Profit and concentrated losses
- **limitation** — cause is not established
- **next step** — collect and compare focused evidence

---

## Ask AI to challenge—not merely write

A useful prompt gives AI a critical role:

> Identify unsupported assumptions, missing evidence and risks in this
> recommendation. Do not rewrite it. Separate criticisms that can be
> checked with the supplied data from those requiring new evidence.

Imagine that the response raises these challenges:

```python
ai_challenges = pd.DataFrame(
    {
        "Challenge": [
            "Low total Profit may partly reflect category size.",
            "The test does not define its duration or success measure.",
            "Supplier contracts may prevent a targeted test.",
            "Furniture customers may dislike all targeted changes.",
        ],
        "Assessment": [
            "Relevant and testable with current data",
            "Relevant decision-design gap",
            "Relevant but requires operational evidence",
            "Too vague to act on without customer evidence",
        ],
        "Response": [
            "Compare margins as well as total Profit",
            "Define scope, period and success threshold",
            "Ask operations before implementation",
            "Request specific evidence or set aside",
        ],
    }
)

ai_challenges
```

The AI response earns attention because each criticism is evaluated—not
because it was produced fluently.

---

## Follow up on a useful challenge

Total Profit can reflect both scale and profitability. Let us compare
Profit margin as an additional measure.

```python
category_evidence["Profit margin"] = (
    category_evidence["Profit"] / category_evidence["Sales"]
)

category_evidence.style.format(
    {
        "Sales": "£{:,.0f}",
        "Profit": "£{:,.0f}",
        "Profit margin": "{:.1%}",
    }
)
```

This check strengthens the analysis because it tests a specific
criticism with relevant evidence.

It may strengthen or weaken the recommendation. Either outcome is
useful.

---

## Revise after challenge

```python
revised_recommendation = (
    "We recommend a time-limited test focused on Tables and Bookcases, "
    "using Profit and Profit margin as success measures. Furniture has the "
    "lowest total Profit, with losses concentrated in those Sub-Categories. "
    "However, the analysis does not establish the cause or include product cost "
    "and returns. Review those fields and operational constraints before any "
    "category-wide action."
)

print(revised_recommendation)
print(f"\nWord count: {len(revised_recommendation.split())}")
```

The challenge changed the recommendation by adding:

- a time boundary
- a second success measure
- an operational check

Revision is part of analysis. A recommendation is not weaker because it
changed after scrutiny.

---

## Your turn — audit a claim

Choose one insight from your Tableau dashboard or an earlier notebook.

Complete this reasoning frame:

```python
my_reasoning = {
    "The chart shows": "",
    "We infer": "",
    "We still need to know": "",
    "Therefore, we recommend": "",
}

pd.Series(my_reasoning, name="My analysis")
```

Then challenge it:

1. Highlight every statement directly supported by the data.
2. Mark each explanation as tested, testable or currently untestable.
3. Generate at least two alternative explanations.
4. Compare an immediate action, a limited test and further analysis.
5. State what evidence would change your recommendation.

If you use AI, ask it to identify assumptions and missing evidence. Audit
each response against the dataset before revising your work.

---

## What Python revealed

Tableau made the pattern visible. Python helped us expose the reasoning
behind a possible decision:

- the category total supported an observation
- Sub-Category detail challenged an overly broad conclusion
- Discount data allowed one possible explanation to be explored
- missing fields defined what we could not establish
- an option table made trade-offs visible
- an AI-style challenge generated questions, not proof
- revision made the recommendation more precise

The central lesson is not about a particular tool.

> **The chart shows…**
>
> **We infer…**
>
> **We still need to know…**
>
> **Therefore, we recommend…**

A defensible decision shows every link.
