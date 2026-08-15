import os
import json
import shutil
from pathlib import Path

# aur-guard app name
APP_NAME = "aur-guard"

def get_config_dir() -> Path:

    """
    Finds and returns the appropriate directory path for config.
    """

    # Get default XDG_CONFIG_HOME
    xdg_config = os.getenv("XDG_CONFIG_HOME")

    # Check for the existence of XDG_CONFIG_HOME value
    if xdg_config:
        return Path(xdg_config) / APP_NAME # return dir path
    
    # Set ~/.config as config dir
    # (if default XDG_CONFIG_HOME value does not exist)
    return Path.home() / ".config" / APP_NAME # return dir path


def setup_config_dir():

    """ 
    Setup config dir and copy default config files
    """

    # Make config file 
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)

    # Set the `source_dir` value to `src/config`
    source_dir = Path(__file__).parent 
    
    # Config files
    config_files = ["config.json", "prompt.json"]

    # Store source file and dest file in two variables
    for file_name in config_files:
        dest_file = config_dir / file_name
        source_file = source_dir / file_name

        # If the file doesn't exist in the dest dir, 
        # copy the default version of the file to the dest dir
        if not dest_file.exists() and source_file.exists():
            shutil.copy(source_file, dest_file)
    return config_dir
        
def load_config_files(file_name: str) -> dict:

    """
    Read config file or prompt from config dir.
    """

    # Find config dir path and then specified file path
    config_dir = setup_config_dir() # get config dir path from setup_config_dir()
    target_file = config_dir / file_name # # set file path

    # return file content
    with open(target_file, "r", encoding="utf-8") as f:
        return json.load(f)