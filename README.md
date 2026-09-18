# ClarityGrid

## A small data-to-decision workspace built from scratch

ClarityGrid is a Python project I built to make the first part of a data analysis job less repetitive.

The idea is simple: give the app a CSV or Excel file, and it helps me move from **raw data → data quality → exploration → useful findings → a simple ML experiment** without jumping between separate notebooks every time.

I did not want this to be a "type your question and an AI magically knows everything" project. The first versions are deliberately transparent. The calculations are visible, the ML models are standard scikit-learn models, and the insight messages are generated from rules that I can explain.

> **Current release:** V1 + selected V2 features  
> **Author:** Trinadh Reddy

---

## Why I built it

When I work with a new dataset, I usually repeat the same steps:

1. load the file;
2. check its shape and columns;
3. find missing and duplicate values;
4. understand numerical and categorical columns;
5. make a few useful plots;
6. look for changes or unusual values;
7. only then decide whether an ML model makes sense.

ClarityGrid puts those steps in one small application.

The project is intentionally focused on **learning and explainability**, rather than pretending to be a replacement for tools such as Power BI, Tableau, or a production ML platform.

---

## What it can do

### V1 — the foundation

- Upload CSV and Excel files
- Inspect rows, columns and data types
- Calculate missing-value and duplicate statistics
- Produce a simple data-quality score
- Separate numerical and categorical columns
- Explore distributions and category counts
- View correlations between numerical columns
- Detect simple time-based trends when a date column is available
- Generate plain-English findings using deterministic rules
- Run a small classification or regression experiment
- Compare a baseline model with a tree-based model
- Show evaluation metrics
- Show feature importance when available
- Export an analysis summary as JSON

### V2 — making the workflow more useful

- SQLite-backed analysis history
- SQL query workspace over the uploaded data
- IQR-based anomaly detection
- Rolling-average trend view
- Simple next-period forecasting using linear regression
- Saved analysis sessions
- More structured insight categories: trend, quality, anomaly and model
- Better validation and error messages

V2 is still deliberately modest. The goal is to add useful engineering and analytics depth without adding technologies that I would not be able to explain in an interview.

---

## Project flow

```text
                 +----------------+
                 | CSV / Excel    |
                 +-------+--------+
                         |
                         v
                 +----------------+
                 | Load + Validate|
                 +-------+--------+
                         |
             +-----------+-----------+
             |                       |
             v                       v
      +-------------+         +-------------+
      | Data Quality|         | Data Profile |
      +------+------+         +------+------+ 
             |                       |
             +-----------+-----------+
                         v
                  +-------------+
                  | Exploration |
                  +------+------+ 
                         |
              +----------+----------+
              |                     |
              v                     v
       +-------------+       +-------------+
       | Rule Insights|       | ML Experiment|
       +-------------+       +-------------+
              |                     |
              +----------+----------+
                         v
                   +-----------+
                   | Decision  |
                   | Summary   |
                   +-----------+
```

---

## Technology choices

I kept the stack intentionally small:

- **Python** — main language
- **Pandas / NumPy** — data handling
- **Matplotlib / Seaborn** — familiar visualizations
- **scikit-learn** — basic ML experiments
- **Streamlit** — simple interactive interface
- **SQLite** — local history in V2
- **Pytest** — tests

I chose these because I can understand the full path from input data to result instead of hiding the important work behind a large framework.

---

## Running it locally

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the app

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

### 4. Run tests

```bash
pytest -q
```

---

## A good first dataset

The repository contains a small sample order dataset in:

`data/sample/orders.csv`

It is intentionally small enough to understand manually. The app is designed to work with other tabular datasets too.

---

## How the quality score works

The quality score is not a machine-learning prediction. It is a transparent checklist converted into a score out of 100.

The score considers:

- missing cells;
- duplicate rows;
- columns with a single unique value;
- whether the dataset can be read successfully.

The calculation is intentionally simple so I can explain every point during an interview.

---

## ML experiment

The ML section is not an AutoML system.

The user selects a target column. The application identifies whether it looks like a classification or regression problem and prepares a basic feature matrix.

For categorical features, V2 uses one-hot encoding. Numerical features are passed through directly. The data is split into training and testing portions using a fixed random seed so that the experiment can be reproduced.

Models used:

- Classification: Logistic Regression and Random Forest
- Regression: Linear Regression and Random Forest Regressor

The application reports metrics appropriate to the task rather than inventing a single universal accuracy number.

---

## What I deliberately did not add yet

I did **not** add an LLM, RAG, vector database, multi-agent workflow, Kubernetes, a cloud data warehouse, or a complicated frontend just to make the project look bigger.

Those technologies can be useful in a later version, but they would make the project harder for me to understand and defend right now.

A future AI-assisted version can sit on top of the existing analysis engine instead of replacing it.

---

## V1 → V2 → future direction

### V1

The goal was to make the basic analysis loop work reliably.

**Input → quality → exploration → findings → ML**

### V2

The goal is to make the application feel more like a small analysis workspace.

**Input → quality → SQL/exploration → trends/anomalies → ML → saved session**

### Future V3 ideas

- PostgreSQL support
- FastAPI backend
- scheduled dataset refresh
- model persistence
- model comparison history
- data drift checks
- explainability with SHAP
- optional natural-language questions over verified analysis results
- downloadable HTML/PDF reports

These are ideas, not claims about the current version.

---

## Limitations

This project is still a student-built analytics application.

- It is designed for tabular datasets that fit into memory.
- Automatic insight rules are intentionally conservative.
- Forecasting is a simple baseline, not a production forecasting service.
- Anomaly detection uses statistical rules and does not understand business context automatically.
- ML preprocessing is basic and should be reviewed for every real dataset.
- Results should be checked by a person before being used for an actual business decision.

I prefer documenting these limitations instead of hiding them.

---

## Repository structure

```text
ClarityGrid/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── app/
│   └── ui.py
├── core/
│   ├── quality.py
│   ├── profiling.py
│   ├── insights.py
│   ├── ml.py
│   ├── trends.py
│   ├── storage.py
│   └── io.py
├── data/
│   └── sample/orders.csv
├── docs/
│   ├── V1.md
│   ├── V2.md
│   ├── PROJECT_DECISIONS.md
│   └── INTERVIEW_NOTES.md
└── tests/
    ├── test_quality.py
    ├── test_insights.py
    └── test_trends.py
```

---

## Project status

This repository is the **new implementation** of ClarityGrid. The previously inspected salary-prediction and hotel-scraping projects were used only as reference material while deciding what problems to avoid and what skills the new project should demonstrate. Their source code, branding, README text and assets are not part of this implementation.

The project is intentionally written in a straightforward style so that the person maintaining it can explain the code rather than treating it as a black box.

---

## License

The original code in this repository is released under the MIT License. Third-party Python packages remain under their respective licenses.
