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
        exploring-data-with-pandas.ipynb
    week-02/
        filtering-sorting-and-grouping.ipynb
    week-03/
        dashboard-storytelling.ipynb
    week-04/
        forecasting-with-python.ipynb
    week-05/
        accessible-and-responsible-visualisation.ipynb
    week-06/
        ai-assisted-data-analysis.ipynb
    week-07/
        interactive-visualisations-with-plotly.ipynb
    week-08/
        explaining-ai-and-ethical-analytics.ipynb
    week-09/
        dashboard-prototyping-with-streamlit.ipynb

data/
    HighStreetRetailData.xlsx

README.md
pyproject.toml
```

Each notebook mirrors the corresponding teaching week and extends the Tableau techniques introduced during the module.

---

## Project Installation

This repository uses **uv**, a modern Python package manager that automatically manages virtual environments and project dependencies.

If you already have Python installed, the entire setup process should take only a few minutes.

### 1. Install Python

Download and install **Python 3.11** or later from:

https://www.python.org/

To check that Python has been installed successfully, open a terminal and run:

```bash
python3 --version
```

or on Windows:

```powershell
python --version
```

You should see something similar to:

```text
Python 3.13.5
```

---

### 2. Install uv

`uv` is a fast, modern replacement for tools such as `pip` and `virtualenv`.

#### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatively, if you already have Python installed:

```bash
pip install uv
```

To verify the installation:

```bash
uv --version
```

---

### 3. Clone the Repository

There are many ways to clone a GitHub repository - below shows one way - it uses the `git` command-line client.

```bash
git clone https://github.com/glowkeeper/data-visualisation-python-companion.git

cd data-visualisation-python-companion
```

---

### 4. Install the Project

This repository includes a `pyproject.toml` file that defines all required Python packages.

Simply run:

```bash
uv sync
```

This command will automatically:

- create a virtual environment (`.venv`) if one does not already exist
- install all required packages
- prepare the notebooks for use

No manual package installation is required.

---

## Running the Notebooks

There are two ways to use the notebooks.

### Option A — Visual Studio Code (Recommended)

If you already use Visual Studio Code, this provides the best experience.

1. Install the **Jupyter** extension from the Extensions Marketplace.
2. Open the `data-visualisation-python-companion` repository in VS Code.
3. Open one of the notebooks, for example:

   ```text
   notebooks/week-01/behind-the-tableau-curtain.ipynb
   ```

4. When prompted, select the project's **.venv** Python interpreter.
5. You can now run cells individually or execute the entire notebook.

Useful toolbar buttons include:

- ▶ **Run Cell** — Executes the current cell.
- ▶▶ **Run All** — Executes every cell from top to bottom.
- 🔄 **Restart** — Restarts the Python kernel if you install additional packages or want to begin again.

Code cells execute in order, so it is usually best to work through the notebook from top to bottom.

---

### Option B — JupyterLab (Browser)

If you prefer, you can run JupyterLab directly from a terminal.

```bash
uv run jupyter lab
```

A browser window should open automatically.

Navigate to:

```text
notebooks/
```

and open the notebook for the appropriate teaching week.

---

## Running Code

Python notebooks are made up of **cells**.

There are two types of cell:

- **Markdown cells** contain explanations and instructions.
- **Code cells** contain executable Python code.

To execute a code cell:

1. Click anywhere inside the cell.
2. Press **Shift + Enter**.

The code will run and any output will appear immediately beneath the cell.

You can also use the **Run Cell** button displayed above each code cell.

---

## Working Through a Notebook

The notebooks are designed to be completed in order.

For each section:

1. Read the explanation.
2. Run the code cell.
3. Examine the output.
4. Complete any **Try it yourself** activities before moving on.

Many of the notebooks encourage experimentation.

If you change some code, simply run the cell again to see the updated result.

---

## How the Notebooks are Organised

Each notebook follows a simple pattern.

1. Introduce the analytical problem.
2. Explain the concept.
3. Demonstrate the Python code.
4. Show the resulting output.
5. Relate the work back to Tableau.
6. Offer an optional extension activity.

The notebooks are intended to be exploratory.

Feel free to modify the code, rerun cells and experiment.

---

## Restarting the Kernel

The Python kernel remembers everything that has been executed.

If you want to begin again from a clean state:

- click **Restart** in VS Code, or
- restart the kernel in JupyterLab.

After restarting, choose **Run All** (or work through the notebook from the beginning) to recreate all variables and outputs.

---

## Updating the Environment

If the repository is updated with additional packages in the future, simply run:

```bash
uv sync
```

again to install any new dependencies.

If you already have a notebook open, restart the kernel afterwards so it can use the newly installed packages.

---

## Troubleshooting

If you experience problems, try:

```bash
uv python list
```

to see the Python installations available on your system.

You can also recreate the environment at any time by deleting the `.venv` directory and running:

```bash
uv sync
```

again.

---

## Relationship to the Module

These notebooks are an **optional companion resource**.

They are **not** required for:

- lectures
- workshops
- Assessment 1
- Assessment 2

Students can successfully complete the module without ever using Python.

The notebooks simply provide an additional perspective for students who would like to explore visual analytics through programming.

---

## Relationship to Tableau

Tableau remains the primary analytical tool used throughout the module.

The notebooks answer questions such as:

- How does Tableau group data?
- How would I filter data in Python?
- How are charts generated programmatically?
- How can repetitive analysis be automated?
- What additional analytical techniques become possible?

The aim is not to replace Tableau, but to understand another way of working with data.

---

## Weekly Themes

| Week | Python Focus |
|------|--------------|
| 1 | Exploring data with pandas |
| 2 | Visualising data with matplotlib |
| 3 | Dashboard storytelling |
| 4 | Forecasting with Python |
| 5 | Accessible and responsible visualisation |
| 6 | AI-assisted data analysis |
| 7 | Interactive visualisations with Plotly |
| 8 | Explaining AI and ethical analytics |
| 9 | Dashboard prototyping with Streamlit |

---

## Contributing

Suggestions and improvements are always welcome.

If you discover an issue or have an idea for a useful extension, please open an issue or submit a pull request.

---

## Licence

This repository is provided as a teaching companion for the **Data Visualisation and Intelligence** module at the University of Roehampton.

Unless otherwise stated, all original material is released under the MIT License.
