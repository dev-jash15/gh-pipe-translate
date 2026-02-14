# 🔄 gh-pipe-translate

**Semantic data pipeline translation directly in your terminal, powered by GitHub Copilot CLI.**

![Demo of gh-pipe-translate](demo.gif) _(Note: Add your screen recording/GIF here!)_

---

## 🛑 The Problem: The Polyglot Pipeline Constraint

Modern data teams are inherently polyglot. Data exploration frequently occurs in statistical libraries (like R's `dplyr` or Python's `pandas`), while production data warehousing demands declarative, scalable languages (like PostgreSQL, Snowflake, or PySpark).

The handoff is painful. Manually translating an analyst's 50-line `dplyr` script—complete with grouped mutations, rolling averages, and lag functions—into a nested SQL query with Common Table Expressions (CTEs) and Window Functions takes a Data Engineer hours. Standard line-by-line translation tools fail because data transformation requires _semantic_ understanding of the logic.

## 💡 The Solution

`gh-pipe-translate` bridges the gap between Data Analysts and Data Engineers. Built as a GitHub CLI extension, it leverages the reasoning engine of **GitHub Copilot CLI** to semantically translate exploratory data scripts into highly optimized, production-ready code without ever leaving the terminal.

### ✨ Features

- **Semantic Translation:** Understands complex data operations (e.g., converting an R `cumsum()` into an SQL `SUM() OVER(ROWS BETWEEN UNBOUNDED PRECEDING...)`).
- **Multi-Target Support:** Translate to `postgres-sql`, `python-pandas`, `pyspark`, and more.
- **Beautiful Terminal UI:** Built with `Rich` for syntax highlighting, loading spinners, and clean error handling.
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

## 🧠 How it Works

This tool was built for the GitHub Copilot CLI Challenge. It treats Copilot not just as a chatbot, but as an embedded reasoning engine.

Under the hood, `gh-pipe-translate` uses a Python wrapper to read the local data file, construct a rigid, context-aware prompt, and programmatically invoke `gh copilot suggest`. It then parses the AI's response, strips out unnecessary markdown, and uses the `Rich` library to format the output natively in the developer's standard workflow.

By eliminating the context-switch of copying code into a browser-based LLM, this extension acts as a true sidekick for Data Engineers.
