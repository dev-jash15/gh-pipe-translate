import typer
import subprocess
import os
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

app = typer.Typer(help="Translate data pipelines across languages using context-aware GitHub Copilot CLI.")
console = Console()

@app.command()
def translate(
    file_path: str = typer.Argument(..., help="Path to the source data script"),
    target: str = typer.Option(..., "--target", "-t", help="Target language/dialect (e.g., postgres-sql)"),
    out: str = typer.Option(None, "--out", "-o", help="Optional: Save the translated code to a file"),
    schema: str = typer.Option(None, "--schema", "-s", help="Inject a database schema file for context-aware naming"),
    with_tests: bool = typer.Option(False, "--with-tests", help="Automatically generate a Data Quality testing file")
):
    """
    Translates a data script into a production-ready target language with context awareness.
    """
    if not os.path.exists(file_path):
        console.print(f"[bold red]Error:[/bold red] File '{file_path}' not found.")
        raise typer.Exit(code=1)

    with open(file_path, 'r') as file:
        source_code = file.read()

    # --- AGENT CONTEXT INJECTION ---
    schema_context = ""
    if schema:
        if not os.path.exists(schema):
            console.print(f"[bold red]Error:[/bold red] Schema file '{schema}' not found.")
            raise typer.Exit(code=1)
        with open(schema, 'r') as s_file:
            schema_context = f"\n\nCRITICAL CONTEXT: You MUST use the exact table names, column names, and data types defined in this schema: \n{s_file.read()}"

    system_prompt = (
        f"You are an expert Data Engineer. Translate the following data analysis script "
        f"into highly optimized, production-ready {target}. "
        f"Only output the raw, translated {target} code. Do not include markdown formatting. "
        f"Do not include explanations. Here is the source code:\n\n{source_code}{schema_context}"
    )

    # --- EXECUTE TRANSLATION ---
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

    # Output Translation
    console.print(Panel.fit(f"[bold green]Translation Complete: ➔ {target.upper()}[/bold green]"))
    syntax_lang = target.split('-')[-1] if '-' in target else target
    syntax = Syntax(translated_code, syntax_lang, theme="monokai", line_numbers=True)
    console.print(syntax)

    if out:
        with open(out, 'w') as f:
            f.write(translated_code)
        console.print(f"\n[bold green]✓ Successfully saved to:[/bold green] {out}")

    # --- EXECUTE DATA QUALITY AGENT ---
    if with_tests:
        test_prompt = (
            f"You are an expert Data Quality Engineer. Based on this {target} code, generate a robust YAML "
            f"data quality testing suite (like dbt schema tests or Great Expectations) to check for nulls, "
            f"unique constraints, and expected values. Output ONLY the raw YAML code. No markdown. "
            f"\n\nCode to test:\n{translated_code}"
        )
        with console.status(f"[bold magenta]Generating Data Quality Tests...[/bold magenta]", spinner="dots"):
            try:
                ps_test_command = f"""copilot -p '{test_prompt.replace("'", "''")}'  -s --allow-all"""
                test_command = ["pwsh", "-NoProfile", "-Command", ps_test_command]
                test_result = subprocess.run(test_command, capture_output=True, text=True, check=True)
                test_code = test_result.stdout.strip()
                
                console.print(Panel.fit("[bold magenta]✓ Data Quality Tests Generated[/bold magenta]"))
                console.print(Syntax(test_code, "yaml", theme="monokai", line_numbers=True))
                
                test_file_name = f"tests_{out.split('/')[-1].split('.')[0]}.yml" if out else "data_quality_tests.yml"
                with open(test_file_name, 'w') as f:
                    f.write(test_code)
                console.print(f"\n[bold green]✓ Successfully saved tests to:[/bold green] {test_file_name}")
                
            except subprocess.CalledProcessError as e:
                console.print("[bold red]Failed to generate tests.[/bold red]")
                console.print(f"Error details: {e.stderr}")

if __name__ == "__main__":
    app()