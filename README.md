# Data Visualisation Python Companion

A companion repository for the **Data Visualisation and Intelligence (DVI)** module at the **University of Roehampton**.

This repository provides **optional Python notebooks** that complement the Tableau-based teaching materials used throughout the module.

The notebooks are **not assessed** and are **not required** to complete the module successfully. They are intended for students who would like to explore how similar analytical tasks can be performed programmatically using Python.

---

## Purpose

The DVI module focuses on transforming:

> **Data → Insight → Decision**

Throughout the module, you will primarily use **Tableau Public** to explore data, build visualisations and communicate analytical insight.

This companion repository explores the same ideas using Python.

Rather than replacing Tableau, these notebooks demonstrate:

- how Tableau operations translate into Python code
- how data can be manipulated programmatically
- how analyses can be automated
- where Python provides capabilities beyond Tableau

The emphasis remains on analytical thinking and communication rather than programming complexity.

---

## Who is this for?

This repository is intended for students who:

- are curious about Python
- would like to explore data science tools
- have some programming experience
- are considering careers involving data analytics or data science

If you have never written Python before, don't worry.

The notebooks are heavily commented and designed to be read as tutorials rather than programming exercises.

---

## Repository Structure

```text
notebooks/
    week-01/
        beyond-tableau.ipynb
    week-02/
        beyond-tableau.ipynb
    week-03/
        beyond-tableau.ipynb
    week-04/
        beyond-tableau.ipynb
    week-05/
        beyond-tableau.ipynb
    week-06/
        beyond-tableau.ipynb
    week-07/
        beyond-tableau.ipynb
    week-08/
        beyond-tableau.ipynb
    week-09/
        beyond-tableau.ipynb
    week-10/
        beyond-tableau.ipynb

data/

README.md
requirements.txt
```

Each weekly notebook follows the rhythm of the taught module and extends the Tableau activities covered during that week's sessions.

---

### Installing Python

If you already have a working Python installation, you can skip this section.

Otherwise, install:

- Python 3.11 or later
- Git
- Visual Studio Code (recommended)

Download Python from:

https://www.python.org/

Download Visual Studio Code from:

https://code.visualstudio.com/

---

## Clone the Repository

```bash
git clone https://github.com/<your-username>/dvi-python-companion.git

cd dvi-python-companion
```

---

## Create a Virtual Environment

### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install the Required Packages

```bash
pip install -r requirements.txt
```

The repository currently uses only a small number of widely used libraries:

- pandas
- matplotlib
- openpyxl
- jupyter

Additional packages may be introduced later as the notebooks become more advanced.

---

## Launch Jupyter

Once everything has been installed, start Jupyter with:

```bash
jupyter notebook
```

or

```bash
jupyter lab
```

A browser window should open automatically.

Navigate to the notebook for the appropriate teaching week and begin working through it.

---

## How the Notebooks are Organised

Each notebook follows a simple pattern.

1. Introduce the analytical problem.
2. Explain the concept.
3. Demonstrate the Python code.
4. Show the resulting output.
5. Relate the work back to Tableau.
6. Offer an optional extension activity.

The notebooks are designed to be exploratory rather than prescriptive.

Feel free to modify the code and experiment.

---

## Relationship to the Module

These notebooks are an **optional companion resource**.

They are **not**:

- required for lectures
- required for workshops
- required for Assessment 1
- required for Assessment 2

Students can achieve excellent marks in the module without ever opening this repository.

The notebooks simply provide an additional route for students who wish to deepen their understanding of visual analytics through programming.

---

## Relationship to Tableau

Throughout the module, Tableau remains the primary analytical tool.

The notebooks are intended to answer questions such as:

- How does Tableau group data?
- How would I filter data in Python?
- How are charts generated programmatically?
- How can repetitive analysis be automated?
- What additional analytical techniques become possible?

The objective is not to replace Tableau, but to understand another way of working with data.

---

## Weekly Themes

| Week | Python Focus |
|------|--------------|
| 1 | Loading and exploring datasets with pandas |
| 2 | Filtering, sorting and grouping data |
| 3 | Creating charts with matplotlib |
| 4 | Trend analysis and forecasting |
| 5 | Data quality and accessibility |
| 6 | AI-assisted analytical workflows |
| 7 | Interactive visualisations |
| 8 | Ethics, transparency and explainability |
| 9 | Project ideas and experimentation |
| 10 | Further study and next steps |

The notebooks may evolve over time to reflect changes to the taught module.

---

## Contributing

Suggestions and improvements are always welcome.

If you discover an issue, spot an error, or have an idea for a useful extension, please open an issue or submit a pull request.

---

## Licence

This repository is provided as a teaching resource for the Data Visualisation and Intelligence module.

Unless otherwise stated, all original material is released under the MIT License.
