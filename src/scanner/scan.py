import os
from pathlib import Path
import shutil
import subprocess
from api.client import run_ai

def run_scan(target: str):
    target_path = Path(target)  # Convert string to Path object

    # --- Check if target is a directory or a URL ---
    if target_path.exists() and target_path.is_dir():
        print("📂 Local directory detected.")
        # under development..
    
    else:
        found_url(target)

def found_url(target):
    # --- Check if target is a URL or package name ---
    if target.startswith("http://") or target.startswith("https://"):
        git_url = target
        clone(git_url)
    else:
        git_url = f"https://aur.archlinux.org/{target}.git"
        clone(git_url)

def clone(git_url):
    # --- Check if git is installed ---
    if not shutil.which("git"):
        return "error: git is not installed."

    # --- Set up target directory ---
    target_name = Path(git_url).stem  # Extract repository name

    target_dir = Path("tmp") / target_name  # Set target directory path
    target_dir.parent.mkdir(parents=True, exist_ok=True)  # Create tmp directory

    # Remove existing target directory
    if target_dir.exists():
        shutil.rmtree(target_dir)
    
    # --- Define Git commands ---
    git_cmds = [
        ["git", "clone", "--filter=blob:none", "--no-checkout", git_url, str(target_dir)],
        ["git", "-C", str(target_dir), "sparse-checkout", "set", "--no-cone", 
         "PKGBUILD", "*.install", "*.patch", "*.diff", "*.sh", "*.service", "*.timer"],
        ["git", "-C", str(target_dir), "checkout"]
    ]

    # --- Run Git commands ---
    for cmd in git_cmds:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    
    text_extract(target_dir)

def text_extract(dir_path: Path):
    output_blocks = []

    # --- Check everything inside directory ---
    for file_path in dir_path.iterdir():

        # Make sure its a file
        if file_path.is_file():
                # Read file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Format the text according to template
                block = f"{file_path.name}:\n```\n{content}\n```\n---"
                output_blocks.append(block)

    # Join all blocks together with a newline in between
    file_contents = "\n\n".join(output_blocks)

    # return output
    run_ai(file_contents)


