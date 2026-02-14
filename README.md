# 🔄 gh-pipe-translate

**Semantic data pipeline translation directly in your terminal, powered by GitHub Copilot CLI.**

![Demo of gh-pipe-translate](demo.gif) _(Note: Add your screen recording/GIF here!)_

---

## 🛑 The Problem: The Polyglot Pipeline Constraint

Modern data teams are inherently polyglot. Data exploration frequently occurs in statistical libraries (like R's `dplyr` or Python's `pandas`), while production data warehousing demands declarative, scalable languages (like PostgreSQL, Snowflake, or PySpark).

The handoff is painful. Manually translating an analyst's 50-line `dplyr` script—complete with grouped mutations, rolling averages, and lag functions—into a nested SQL query with Common Table Expressions (CTEs) and Window Functions takes a Data Engineer hours. Standard line-by-line translation tools fail because data transformation requires _semantic_ understanding of the logic.

## 💡 The Solution

`gh-pipe-translate` bridges the gap between Data Analysts and Data Engineers. Built as a GitHub CLI extension, it leverages the reasoning engine of **GitHub Copilot CLI** to semantically translate exploratory data scripts into highly optimized, production-ready code without ever leaving the terminal.

Going beyond simple wrappers, this tool operates as an **Agentic Workflow**, capable of mapping your destination database and automatically writing data quality tests.

### ✨ Features

- **Semantic Translation:** Understands complex data operations (e.g., converting an R `cumsum()` into an SQL `SUM() OVER(ROWS BETWEEN UNBOUNDED PRECEDING...)`).
- **Context-Awareness (`--schema`):** Inject your database schema to ensure translated code uses the exact table names, column names, and data types of your production environment.
- **Data Quality Agent (`--with-tests`):** Automatically spawns a secondary AI agent to write robust YAML testing suites (e.g., dbt, Great Expectations) for the newly translated pipeline.
- **Multi-Target Support:** Translate to `postgres-sql`, `python-pandas`, `pyspark`, and more.
- **File I/O Ready:** Instantly write production-ready code to your local directory using the `--out` flag.

---

## ⚙️ Installation

**Prerequisites:**

1. [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated (`gh auth login`).
2. GitHub Copilot enabled on your account.
3. Python 3.10+ installed on your system.

**Install the Extension:**

```bash
# Install directly from GitHub
gh extension install dev-jash15/gh-pipe-translate
```

(Upon first run, the tool will automatically install its lightweight UI dependencies: `typer` and `rich`.)

## 🚀 Usage

The basic syntax requires a source file and a `--target` language flag.

```bash
gh pipe-translate <source_file> --target <target_language>
```

**Example 1: Terminal Preview**

Translate an R script to PostgreSQL and preview it in the terminal with full syntax highlighting:

```bash
gh pipe-translate examples/complex_analysis.R --target postgres-sql
```

**Example 2: Save to Production**

Translate the same logic into a Python script using Pandas, and save it directly to your project directory:

```bash
gh pipe-translate examples/complex_analysis.R --target python-pandas --out prod_pipeline.py
```

**Example 3: The Enterprise Agent (Schema + Tests)**

Inject your production database schema to ensure perfectly mapped column names, and automatically generate a data quality testing suite in one command:

```bash
gh pipe-translate examples/complex_analysis.R --target postgres-sql --out examples/prod_pipeline.sql --schema examples/schema.sql --with-tests
```

## 🧠 How it Works

This tool was built for the GitHub Copilot CLI Challenge. It treats Copilot not just as a chatbot, but as an embedded reasoning engine capable of multi-step agentic workflows.

Under the hood, `gh-pipe-translate` uses a Python wrapper to read local data files and construct rigid, context-aware prompts. When flags like `--schema` and `--with-tests` are used, the extension orchestrates sequential programmatic calls to `gh copilot suggest` — first mapping the architecture, then executing the translation, and finally spinning up a secondary agent to write the YAML quality tests.

By eliminating the context-switch of copying code into a browser-based LLM, this extension acts as a true sidekick for Data Engineers.
