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
