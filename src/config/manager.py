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

def load_config_file(file_name: str) -> dict:

    """
    Read config file or prompt from config dir.
    """

    # Find config dir path and then specified file path
    config_dir = setup_config_dir() # get config dir path from setup_config_dir()
    target_file = config_dir / file_name # set file path

    # if target file doesn't exist, create it
    if not target_file.exists():
        setup_config_dir()

    # return file content
    with open(target_file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_config_json_path():
    # Find config dir path and then specified file path
    config_dir = setup_config_dir() # get config dir path from setup_config_dir()
    target_file = config_dir / "config.json" # get file path 

    return(target_file)

def check_api_section(config, target_file):

    # raise KeyError if 'api' doesn't exist in config file
    if 'api' not in config:
        raise KeyError(f"API section missing in {target_file}.")

    # if present but not a dict, raise TypeError
    if not isinstance(config['api'], dict):
        raise TypeError(f"API section in {target_file} must be a dictionary, got {type(config['api']).__name__}.")

def set_base_url(base_url: str):
    
    """
    Update `base_url` in `config.json`
    """
    
    target_file = get_config_json_path() # get config file path
    
    # Read file content
    with open(target_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # raise KeyError if 'api' doesn't exist in config file
    if 'api' not in config:
        raise KeyError(f"API section missing in {target_file}.")

    # if present but not a dict, raise TypeError
    if not isinstance(config['api'], dict):
        raise TypeError(f"API section in {target_file} must be a dictionary, got {type(config['api']).__name__}.")

    # Updating the value of `['base_url']` in ram
    config['api']['base_url'] = base_url

    # Writing to file
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
        return(target_file)
    
def set_model(model: str):

    """
    Update `base_url` in `config.json`
    """

    target_file = get_config_json_path() # get config file path

    # Read file content
    with open(target_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # raise KeyError if 'api' doesn't exist in config file
    if 'api' not in config:
        raise KeyError(f"API section missing in {target_file}.")

    # if present but not a dict, raise TypeError
    if not isinstance(config['api'], dict):
        raise TypeError(f"API section in {target_file} must be a dictionary, got {type(config['api']).__name__}.")
    
    # Updating the value of `['model']` in ram
    config['api']['model'] = model

    # Writing to file
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
        return(target_file)

def set_default_sensitivity(default_sensitivity: str):
    if default_sensitivity in ("low", "medium", "high"):

        target_file = get_config_json_path() # get config file path

        # Read file content
        with open(target_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        check_api_section(config, target_file) 

        # Updating the value of `['default_sensitivity']` in ram
        config['api']['default_sensitivity'] = default_sensitivity

        # Writing to file
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            return(target_file)
    else:
        raise ValueError(f"Invalid sensitivity level: '{default_sensitivity}'. Expected 'low', 'medium', or 'high'.")