import typer
from pathlib import Path
from dotenv import find_dotenv, set_key
from scanner.scan import run_scan
from config.manager import set_base_url

# --- App Initialization ---

# Main Typer app instance
app = typer.Typer(
    help="aur-guard: AI security auditor for PKGBUILD files", no_args_is_help=True
)

# Subcommand group for @config
config = typer.Typer(
    help="Manage API keys and app settings", no_args_is_help=True
)

app.add_typer(config, name="config")

# --- @config Commands ---

# @config api command
@config.command(name="api")
def set_api_key(key: str):

    """Save or update the API key in the .env file.""" # help message

    # Locate/create the .env file in the project root directory
    env_path = Path(__file__).resolve().parent.parent / ".env"
    env_path.touch(exist_ok=True)
    
    # Save the API key in .env file
    set_key(str(env_path), "AUR_GUARD_API_KEY", key)

    typer.secho(f"✅ API key saved successfully to {env_path}", fg=typer.colors.GREEN)

# @config url command
@config.command(name="url")
def url(url: str):
    
    """Update base_url in config file"""

    try:
        target_file = set_base_url(url)
        typer.secho(f"✅ URL saved successfully to {target_file}", fg=typer.colors.GREEN)
    
    except (KeyError, TypeError) as e:
        typer.secho(f"❌ Configuration Error: {e}", fg=typer.colors.RED, err=True)

# --- @app Commands ---

# @app scan command
@app.command(name="scan")
def scan(target: str):

    """Scan an AUR package or local directory."""

    typer.secho(f"🔍 Analyzing target: {target}..", fg=typer.colors.CYAN)
    run_scan(target)

    

# Entry point
if __name__ == "__main__":
    app()
