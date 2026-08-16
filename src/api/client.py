import os
import json
import requests
from pathlib import Path
from config.manager import load_config_file

def run_ai(file_contents: str):
    # --- Load environment variables ---
    load_env()

    api_key = os.environ.get("AUR_GUARD_API_KEY")
    if not api_key:
        print("error: AUR_GUARD_API_KEY is not set in the .env file.")
        return None

    # --- Load configurations ---
    config = load_config_file("config.json")
    prompt_config = load_config_file("prompt.json")

    # --- Set up API details ---
    api_settings = config.get("api", {})
    base_url = api_settings.get("base_url", "https://api.openai.com/v1")
    model = api_settings.get("model", "gpt-4o-mini")
    timeout = api_settings.get("timeout", 15)
    print(config, prompt_config, api_settings, base_url, model, timeout)
    # --- Build the prompt text ---
    sensitivity = config.get("default_sensitivity", "medium")
    
    # Extract the specific prompt based on the configured sensitivity level
    level_prompt = prompt_config.get("levels", {}).get(sensitivity, {}).get("prompt", "")
    
    # Combine the main prompt from prompt.json with the provided file contents
    combined_user_prompt = f"{level_prompt}\n\n{file_contents}"

    # Build the system prompt using base instructions and the expected schema
    system_base = prompt_config.get("system_base", "")
    schema = json.dumps(prompt_config.get("output_schema", {}), indent=2)
    system_prompt = f"{system_base}\n\nOutput Schema:\n{schema}"

    # --- Prepare the API request ---
    endpoint = f"{base_url}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_user_prompt}
        ]
    }

    # --- Send the request to the AI model ---
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()  # Check for HTTP errors
        
        # Extract the text content from the AI response
        result_data = response.json()
        ai_response = result_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Print the final response
        print(ai_response)
        
        return ai_response

    except requests.exceptions.RequestException as e:
        print(f"error: API request failed - {e}")
        return None


def load_env():
    # --- Parse .env file manually to keep dependencies simple ---
    env_path = Path(".env")
    if not env_path.exists():
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                
                # Remove whitespace and surrounding quotes
                key = key.strip()
                val = val.strip().strip("'").strip('"')
                
                # Set environment variable
                os.environ[key] = val


def load_json(filepath: str):
    # --- Read and parse a JSON configuration file ---
    path = Path(filepath)
    if not path.exists():
        print(f"error: configuration file not found at {filepath}")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
