# Project Data Visualisation — recovered context

Recovered read-only from the signed-in ChatGPT web conversation **DVI Workshop Structure** on 14 July 2026.

Source conversation: <https://chatgpt.com/c/6a305966-bb58-83ed-bbcf-44f461d05575>

## Project purpose and teaching approach

Data Visualisation (DVI) is a teaching/module-development project built around the progression **Data → Insight → Decision**. Tableau remains central, while the Python/Jupyter material is intended to reveal the analytical ideas that Tableau can hide—not become a separate Python-programming course.

The notebooks are designed as analytical conversations. Weeks 1 and 2 explain what Tableau does; Week 3 shifts toward what analysts do and is framed as **Dashboard Storytelling**. A dashboard is treated as a narrative that answers a question, rather than merely several charts on one page.

## Main module materials

The conversation contains or references these core source documents:

- `Curriculum Overview.md`
- `Design Principles.md`
- `Module Resources and Delivery Guide.md`
- `Module Summary.md`
- `Tutor Handbook.md`
- The repository `README.md`
- Weekly overview and export material, including `week-07-overview.md` and `export-week.sh`

## Assessments and export pipeline

There are two principal assessment briefs:

1. **Assessment 1 — Individual Report**
2. **Assessment 2 — Final Project and Presentation** (also described as a Data Visualisation Project and Board Presentation)

The briefs must match the Roehampton/university assessment template. Work in the conversation covered:

- Exact template structure and front-table presentation
- Placeholder replacement rather than appending content after the template
- Shading, table borders, headings, learning-outcome labels and paragraph spacing
- DOCX generation through `export_assessment_brief_docx.py`, `export_docs.rb`, `export-docs.sh` and related scripts
- Rubric generation through `export_rubric_xlsx.py`
- Matching the continuing-education rubric template, including a separate `100` column and additional fail columns

The last explicitly accepted assessment-brief outputs were:

- `Assessment 1 — Individual Report(18).docx`
- `Assessment 2 — Final Project and Presentation(19).docx`

They were considered good enough to submit: placeholders and duplicate template content were gone, the front table and DVI content were correct, and formatting was consistent. Markdown tables were still rendered as text rather than native Word tables, but further exporter changes were considered too risky at that point.

The later empty-rubric export problem was fixed after comparing the DVI Markdown rubrics with the DA&RS variants and updating the regex/export script.

## Python and Jupyter companion work

The project includes Jupytext-authored Markdown notebooks, generated into `.ipynb` files and run either:

- In the browser, or
- In VS Code with the Jupyter extension and the project `.venv` selected as the kernel

Markdown is intended to remain the source of truth. The workflow is to regenerate the notebook with Jupytext, open the `.ipynb`, select the correct kernel, and use **Run All** or **Shift+Enter**.

The latest notebook direction was:

- Keep the notebooks aligned to the module rhythm and overview documents.
- Week 3 should be **Dashboard Storytelling**.
- Use fewer new Python concepts in Week 3 and more reflective “Think” moments.
- Teach that charts provide evidence while the story provides meaning.
- Update the repository README with explicit browser and VS Code/Jupyter instructions.

Files attached near this work included:

- `README(16).md` and `README(17).md`
- `behind-the-tableau-curtain.md`
- `filtering-sorting-and-grouping.md`
- Updated copies of the five module-overview documents

## Tableau support captured in the conversation

Recent work also covered a Tableau teaching slide and live troubleshooting around:

- Creating a dual axis
- Synchronising axes
- Dropping Sales onto the correct Marks card rather than only creating a legend
- Editing category colour on the appropriate Marks card

## Current handover state

- The cloud material has not been deleted; it lives in a long ChatGPT conversation rather than a ChatGPT Project container.
- The assessment briefs reached an accepted/stable output state. Avoid changing the exporter without regression-testing against the accepted `(18)` and `(19)` documents.
- Rubric generation was fixed after the empty-output regression.
- The Jupyter companion notebooks were working and positively received for teaching.
- The most recent conceptual task was the Week 3 Dashboard Storytelling notebook and the Jupytext generation workflow.
- The source conversation contains many attached scripts, documents, spreadsheets and Markdown files. This note indexes their role but is not a byte-for-byte export of those attachments.
