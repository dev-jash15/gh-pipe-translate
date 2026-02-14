import typer
import subprocess
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
import os

# Initialize Typer app and Rich console
app = typer.Typer(help="Translate data pipelines across languages using GitHub Copilot CLI.")
console = Console()

@app.command()
def translate(
    file_path: str = typer.Argument(..., help="Path to the source data script (e.g., script.R, analysis.py)"),
    target: str = typer.Option(..., "--target", "-t", help="Target language/dialect (e.g., postgres-sql, pyspark, python)"),
    out: str = typer.Option(None, "--out", "-o", help="Optional: Save the output to a file")
):
    """
    Translates a data script into a production-ready target language.
    """
    # 1. Verify the file exists
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error:[/bold red] File '{file_path}' not found.")
        raise typer.Exit(code=1)

    # 2. Read the source code
    with open(file_path, 'r') as file:
        source_code = file.read()

    # 3. Construct the strict AI Prompt
    system_prompt = (
        f"You are an expert Data Engineer. Translate the following data analysis script "
        f"into highly optimized, production-ready {target}. "
        f"Only output the raw, translated {target} code. Do not include markdown formatting like ```sql or ```python. "
        f"Do not include any explanations. Here is the source code:\n\n{source_code}"
    )

    # 4. Execute Copilot CLI with a UI Spinner
    with console.status(f"[bold cyan]Analyzing logic and translating to {target}...[/bold cyan]", spinner="dots"):
        try:
            # Use the Copilot CLI in non-interactive mode with -p flag
            # On Windows, copilot is a PowerShell script, so use pwsh to run it
            # Use single quotes to avoid escaping issues with the prompt
            ps_command = f"""copilot -p '{system_prompt.replace("'", "''")}'  -s --allow-all"""
            command = ["pwsh", "-NoProfile", "-Command", ps_command]
            
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            translated_code = result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            console.print("[bold red]Translation failed.[/bold red] Ensure GitHub Copilot CLI is authenticated.")
            console.print(f"Error details: {e.stderr}")
            raise typer.Exit(code=1)

    # 5. Output the result beautifully
    console.print(Panel.fit(f"[bold green]Translation Complete: ➔ {target.upper()}[/bold green]"))
    
    # Render the output with syntax highlighting
    syntax_lang = target.split('-')[-1] if '-' in target else target # e.g., postgres-sql -> sql
    syntax = Syntax(translated_code, syntax_lang, theme="monokai", line_numbers=True)
    console.print(syntax)

    # 6. Save to file if --out is provided
    if out:
        try:
            with open(out, 'w') as f:
                f.write(translated_code)
            console.print(f"\n[bold green]✓ Successfully saved to:[/bold green] {out}")
        except Exception as e:
            console.print(f"\n[bold red]Failed to save file:[/bold red] {e}")

if __name__ == "__main__":
    app()