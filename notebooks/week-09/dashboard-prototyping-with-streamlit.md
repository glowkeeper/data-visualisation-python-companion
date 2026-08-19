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

# Week 9 — Behind the Tableau Curtain

## Dashboard Prototyping with Streamlit

Week 7 asked whether an interaction was **useful**. Week 8 asked what an
analysis **could not tell you**. This week the question is about the whole
artefact:

> **If you deleted this chart, would anyone decide differently?**

Most weak dashboards are not wrong. They are *unfocused* — three questions
answered adequately instead of one question answered well. Tableau makes adding
another sheet cheap, so the cost of that drift is hidden until someone has to
stand up and defend the result.

Prototyping in code makes the cost visible. A Streamlit app is a script: every
chart is a line you had to write, and every control is a variable you had to
name. Nothing appears because it was easy to drag.

This notebook runs the module's chain **backwards**, because that is how a
dashboard is designed rather than discovered:

> **Decision → Question → Insight → Evidence → Interaction**

The Python companion is optional and unassessed. You do not need to run it to
benefit from reading it.

---

## Load the retail data

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.ticker import FuncFormatter

DATASET = "../../data/HighStreetRetailData.xlsx"

df = pd.read_excel(DATASET)
df["Order Date"] = pd.to_datetime(df["Order Date"])

print(f"Rows: {len(df):,}")
df[["Order Date", "Category", "Sub-Category", "Sales", "Discount", "Profit"]].head()
```

The colour rules from Week 5 still apply, and this notebook keeps the Week 8
palette: blue and orange rather than green and orange, so that the pairing
survives protanopia, and never colour alone to carry a reading.

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

## Start at the end: name the decision

A dashboard is not a report with buttons. It is a tool someone uses to *do*
something. So the first question is not "what does the data show?" but "what is
the person looking at this about to change?"

Write the decision before writing any code.

```python
brief = {
    "Who uses this": "Category manager, reviewing furniture trading monthly",
    "Decision they make": "Whether to keep authorising deep discounts on Tables",
    "What they can change": "The maximum discount sales staff may approve",
    "When they decide": "Monthly trading review",
    "What would change their mind": "Evidence that deep discounts win volume that pays for itself",
}

pd.Series(brief, name="Assessment 2 — dashboard brief").to_frame()
```

Notice the last row. If you cannot say what evidence would *change* the
decision, you are building a dashboard that can only confirm what you already
think — and the board will find that out in about ninety seconds.

> **Think:** For your own project, can you name the person, the decision and the
> lever they control? If the answer is "anyone interested in the data", you do
> not yet have a dashboard brief.

---

## One question, narrow enough to be answered wrongly

A good dashboard question is falsifiable. "How is Furniture performing?" cannot
be answered wrongly, so it cannot be answered usefully either.

```python
questions = pd.DataFrame(
    [
        ("How is Furniture performing?", "No", "No measure, no threshold, no decision"),
        ("Which sub-category is worst?", "Yes", "Answerable, but leads nowhere"),
        ("Does discounting Tables above 30% pay for itself?", "Yes", "Names a lever and a threshold"),
    ],
    columns=["Candidate question", "Falsifiable", "Why"],
)

questions
```

The third question earns its place because a *number* can settle it, and the
answer points at an action. Hold on to it: everything the prototype contains
must serve it, and everything that does not serve it is decoration.

---

## Find one insight, and word it honestly

Week 9's workshop contrasts three ways of stating the same finding. It is worth
doing that arithmetic here, because the wording you can defend depends on what
the data actually supports.

```python
tables = df[df["Sub-Category"] == "Tables"]

sales = tables["Sales"].sum()
profit = tables["Profit"].sum()
loss_share = (tables["Profit"] < 0).mean()

print(f"Tables — sales:  £{sales:,.0f}")
print(f"Tables — profit: £{profit:,.0f}")
print(f"Loss-making order lines: {loss_share:.0%}")
```

Tables sell well and lose money. Now the discount picture:

```python
BANDS = [-0.01, 0.001, 0.15, 0.30, 0.50, 1.0]
LABELS = ["0%", "1–15%", "16–30%", "31–50%", ">50%"]

banded = tables.assign(Band=pd.cut(tables["Discount"], BANDS, labels=LABELS))

by_band = (
    banded.groupby("Band", observed=True)
    .agg(Lines=("Profit", "size"), Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .round(0)
)

by_band
```

Three statements of the same result:

```python
wording = pd.DataFrame(
    [
        ("Vague", "Furniture underperforms", "True of almost any category, so it directs nothing"),
        ("Overclaimed", "Deep discounts cause Tables to lose money", "Asserts cause; the data shows association"),
        ("Defensible", "Tables are profitable undiscounted and lose money above 30%; "
                       "discounting is the strongest available explanation, untested", "Matches the evidence"),
    ],
    columns=["Wording", "Claim", "Why"],
)

wording
```

The defensible version is longer, and that is the point. Week 6 and Week 8 both
warned against asserting a cause the data cannot establish. Nothing here rules
out the alternative — that hard-to-shift stock gets discounted *because* it was
already unprofitable.

> **Think:** Which of your own project's claims asserts a cause? What experiment
> or extra field would be needed to earn that verb?

---

## The evidence: one chart that carries the claim

If the insight is real, one chart should make it obvious. Build that chart
first, in isolation, before deciding anything about layout or controls.

```python
plot_data = by_band[by_band["Lines"] > 0]
colours = [GAIN if value >= 0 else LOSS for value in plot_data["Profit"]]

fig, ax = plt.subplots(figsize=(7.2, 3.8))
bars = ax.bar(plot_data.index.astype(str), plot_data["Profit"], color=colours)

ax.axhline(0, color="#444444", linewidth=0.9)
ax.set_title("Tables: profit by discount band", loc="left", fontsize=12)
ax.set_xlabel("Discount applied")
ax.set_ylabel("Profit")
ax.yaxis.set_major_formatter(MONEY)

for bar, value in zip(bars, plot_data["Profit"]):
    offset = 900 if value >= 0 else -1800
    ax.text(bar.get_x() + bar.get_width() / 2, value + offset,
            f"£{value:,.0f}", ha="center", fontsize=9)

tidy(ax)
plt.tight_layout()
plt.show()
```

The sign is carried by position relative to zero *and* by the printed figure, so
the chart still reads if the colours fail.

One chart, one claim. That is the standard the rest of the prototype has to
meet.

---

## Does the pattern hold outside Tables?

A board member will ask whether you found a rule or a coincidence. Check before
they do.

```python
whole = df.assign(Band=pd.cut(df["Discount"], BANDS, labels=LABELS))

overall = (
    whole.groupby("Band", observed=True)
    .agg(Lines=("Profit", "size"), Sales=("Sales", "sum"), Profit=("Profit", "sum"))
)
overall["Margin %"] = (overall["Profit"] / overall["Sales"] * 100).round(1)

overall.round(0)
```

The threshold is not a quirk of Tables: across the whole dataset, margin falls
away as discounting deepens and turns negative in the upper bands. That makes
the finding more useful — and raises a larger question than the one this
dashboard was scoped to answer.

Resist it. A dashboard that answers one question well is worth more than one
that gestures at three.

---

## What the prototype must contain

Before writing the app, list the minimum that answers the question. Then treat
the list as a budget, not a starting point.

```python
spec = pd.DataFrame(
    [
        ("Headline figures", "Sales, profit and margin for the selection", "States the problem"),
        ("Profit by discount band", "The chart above", "Carries the claim"),
        ("Discount ceiling control", "Slider the manager can move", "Tests the lever they control"),
        ("Limitation note", "What the data cannot show", "Prevents overreach"),
    ],
    columns=["Element", "What it is", "Why it earns its place"],
)

spec
```

Four elements. No trend line, no map, no customer breakdown — not because those
are bad, but because none of them changes the decision this dashboard exists to
support.

---

## The prototype

Streamlit turns a Python script into a web app: `st.metric` draws a figure tile,
`st.slider` creates a control, and the whole script re-runs whenever the reader
moves it. That re-run model is the useful part — the app has no hidden state, so
what the reader sees is always the direct consequence of the inputs.

We write the app to a file rather than running it inside the notebook, because a
Streamlit app is a *separate artefact*: the thing you would hand to the manager.

```python
APP = Path("dashboard_prototype.py")

APP.write_text('''
"""Week 9 prototype — does discounting Tables above 30% pay for itself?

Run with:  streamlit run dashboard_prototype.py
"""

import pandas as pd
import streamlit as st

DATASET = "../../data/HighStreetRetailData.xlsx"
BANDS = [-0.01, 0.001, 0.15, 0.30, 0.50, 1.0]
LABELS = ["0%", "1-15%", "16-30%", "31-50%", ">50%"]


@st.cache_data
def load():
    frame = pd.read_excel(DATASET)
    frame["Order Date"] = pd.to_datetime(frame["Order Date"])
    return frame


df = load()

st.title("Does discounting Tables above 30% pay for itself?")
st.caption("Prototype for the monthly trading review — High Street Retail data")

ceiling = st.slider(
    "Maximum discount authorised",
    min_value=0, max_value=80, value=50, step=5,
    help="Show trade that would still be permitted under this ceiling.",
    format="%d%%",
)

tables = df[df["Sub-Category"] == "Tables"]
allowed = tables[tables["Discount"] <= ceiling / 100]

sales = allowed["Sales"].sum()
profit = allowed["Profit"].sum()
margin = (profit / sales * 100) if sales else 0.0

left, middle, right = st.columns(3)
left.metric("Sales", f"£{sales:,.0f}")
middle.metric("Profit", f"£{profit:,.0f}")
right.metric("Margin", f"{margin:.1f}%")

st.subheader("Profit by discount band")

banded = (
    allowed.assign(Band=pd.cut(allowed["Discount"], BANDS, labels=LABELS))
    .groupby("Band", observed=True)["Profit"]
    .sum()
)

st.bar_chart(banded, color="#3b6ea5" if profit >= 0 else "#c55a11")

st.caption(
    f"At a {ceiling}% ceiling, Tables trade turns "
    f"{'a profit' if profit >= 0 else 'a loss'} of £{abs(profit):,.0f}."
)

st.divider()
st.subheader("What this cannot tell you")
st.markdown(
    """
- The data records **no cost of holding stock**, so "unsold" is not costed here.
- Returns and refunds are absent, so profit is **gross of returns**.
- Discounts may be a **response** to slow-moving stock rather than its cause.
- Removing deep discounts may lose the volume entirely, not convert it.
"""
)
''')

print(f"Written: {APP.resolve().name} ({APP.stat().st_size:,} bytes)")
```

Run it from a terminal, in this folder, with the project environment active:

```text
streamlit run dashboard_prototype.py
```

The limitation panel is not an apology. It is the part that survives contact
with a board, and writing it *into the artefact* means the caveat travels with
the number instead of living in your head.

---

## Every control must earn its place

The slider looks harmless. Test it the way Week 7 tested interactions: what
question does it answer, and what happens if it is removed?

```python
def trade_at(ceiling):
    allowed = tables[tables["Discount"] <= ceiling / 100]
    sales = allowed["Sales"].sum()
    profit = allowed["Profit"].sum()
    return {
        "Ceiling": f"{ceiling}%",
        "Sales": round(sales),
        "Profit": round(profit),
        "Margin %": round(profit / sales * 100, 1) if sales else 0.0,
    }


pd.DataFrame([trade_at(c) for c in (0, 15, 30, 50, 80)])
```

The control earns its place: moving it flips the sign of the answer, and the
ceiling is precisely what the manager controls. A filter that only ever makes
the same number smaller would not have passed this test.

> **Think:** Take each control in your Tableau dashboard. Which value of it
> would change the recommendation? If none would, the control is decoration.

There is a trap in that table worth naming. It shows what the *past* would have
looked like under a ceiling — not what the future will look like once one is
imposed. Removing a 40% discount does not convert that sale to 30%; it may
remove the sale.

---

## The AI-assisted capability, named and evaluated

Assessment 2 requires at least one AI-assisted analytical capability that is
**evaluated and justified**. Modest and understood beats impressive and opaque.

Here the capability is a simple classifier of at-risk trade: which order lines
resemble those that historically lost money.

```python
from sklearn.tree import DecisionTreeClassifier, export_text

features = ["Discount", "Quantity", "Sales"]
X = tables[features]
y = (tables["Profit"] < 0).astype(int)

model = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X, y)

print(export_text(model, feature_names=features))
print(f"Accuracy on the data it was fitted to: {model.score(X, y):.1%}")
```

A depth-2 tree is deliberately shallow: you can read the whole rule, which means
you can defend it. Read the output carefully and it says three useful things
before you have scored it at all.

```python
depth1 = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y)

print(f"Split used at the root: Discount <= {model.tree_.threshold[0]:.2f}")
print(f"Depth-1 score: {depth1.score(X, y):.1%}   Depth-2 score: {model.score(X, y):.1%}\n")

pd.Series(dict(zip(features, model.feature_importances_)), name="Importance").to_frame()
```

First, only `Discount` is used — `Quantity` and `Sales` carry zero importance, so
two of the three inputs contribute nothing. Second, depth-2 scores exactly the
same as depth-1, so the extra layer is decoration; the model is really a single
rule. Third, its own boundary falls at **25%**, not the 30% chosen by eye from
the banded table.

That third point is the one to take to the board. A round number picked from a
chart and a threshold learned from the data disagree slightly, and neither is
authoritative — the honest recommendation names a ceiling *and* the range over
which the evidence is ambiguous.

Now answer the five questions from the Week 8 analysis card — the same five the
CTO will ask.

```python
card = {
    "What data it used": "326 Tables order lines; discount, quantity and line value",
    "What method produced it": "Decision tree classifying loss-making lines; effectively one rule on Discount",
    "What assumptions it makes": "Past line-level patterns persist; discount alone carries the signal",
    "What it cannot tell you": "Nothing causal, and nothing about lines it never saw",
    "How confident, and why": "Low — scored on its own training data, so this is fit, not accuracy",
}

pd.Series(card, name="AI-assisted capability — analysis card").to_frame()
```

That last row is the honest one. A score measured on the data the model was
fitted to is not a measure of performance, and saying so is worth more marks
than a larger number you cannot defend.

> **AI suggests. The analyst evaluates. The analyst decides — and the analyst
> answers for it.**

---

## From prototype to the Design and Development Summary

The brief asks for a **one-page** Design and Development Summary — a
justification of your decisions, not a diary of your week. The prototype has
already generated most of it, because every element had to argue for inclusion.

```python
summary = {
    "Objective": "Support a monthly decision on the discount ceiling for Tables",
    "Key design decision": "One question per dashboard; three candidate charts cut",
    "Technical choice": "Streamlit prototype — controls are explicit and re-runs are stateless",
    "AI-assisted capability": "Depth-2 decision tree, chosen for readability over accuracy",
    "Challenge encountered": "Discount and profitability are associated; direction unproven",
    "Lesson learned": "A ceiling applied to past trade is not a forecast of future trade",
    "Future improvement": "Join stock-holding cost and returns to close the causal gap",
}

pd.Series(summary, name="Design and Development Summary — skeleton").to_frame()
```

Each line follows the shape the workshop asks for: **I chose X because Y, which
the evidence supports.** None of them describes what you did on Tuesday.

---

## Facing the board

Assessment 2 ends with a structured board discussion, and it is assessed. Run
the three perspectives against your own prototype now, while you can still
change it.

```python
board = pd.DataFrame(
    [
        ("Director of Operations and Decision Making",
         "What should we actually do, and what is it worth?",
         "Cap authorised discount on Tables at 30%; £27k of losses sat above it"),
        ("Chief Technology Officer",
         "Why did you build it that way?",
         "One question, four elements; the tree is depth-2 so the rule is readable"),
        ("Director of Strategy, Risk and Ethics",
         "What can your analysis not tell us?",
         "Direction of causation, returns, holding cost, and lost volume"),
    ],
    columns=["Board member", "What they press on", "Your prepared answer"],
)

board
```

Notice that every prepared answer came from work already done above. Preparation
for the board is not a separate exercise bolted on at the end — it is what a
defensible analysis produces on the way through.

> **Think:** Which of these three would you least like to face? That is where
> your preparation is thinnest.

---

## Your turn — prototype your own project

Use your own Assessment 2 dataset and question.

```python
my_brief = {
    "Who uses this": "",
    "Decision they make": "",
    "What they can change": "",
    "My question, stated so it could be answered wrongly": "",
    "My insight, worded so I can defend the verb": "",
    "The one chart that carries it": "",
    "My AI-assisted capability, and its weakest assumption": "",
    "What my dashboard cannot tell anyone": "",
}

pd.Series(my_brief, name="My project brief").to_frame()
```

Then:

1. List every chart and control in your Tableau dashboard.
2. For each, name the question it answers and the decision it changes.
3. Delete anything that cannot answer both. Count what you removed.
4. Write your limitation note *into* the dashboard, not just your summary.

If you use AI, ask it to attack the design rather than produce it:

> *Here is my dashboard question, my insight and my list of charts. Which charts
> do not serve the question, and what would a sceptical board member ask first?*

Then judge each suggestion against your data. A confident critique is still only
a suggestion.

---

## What Python revealed

Tableau makes a dashboard easy to assemble. Writing one as a script exposed the
decisions that assembly hides:

- the brief had to name a person, a decision and a lever before any code existed
- a question that cannot be answered wrongly cannot be answered usefully
- the defensible wording was longer than the overclaimed one, and survived
- one chart carried the claim; three candidate charts did not survive the budget
- the control earned its place because moving it flipped the sign of the answer
- a ceiling applied to past trade is not a prediction about future trade
- a shallow model was readable enough to show that two of its inputs did nothing
- the model's own threshold and the one chosen by eye disagreed, and both were reported
- the limitation note became part of the artefact rather than part of the talk

> **A dashboard is not finished when there is nothing left to add. It is
> finished when there is nothing left that fails to change a decision.**
