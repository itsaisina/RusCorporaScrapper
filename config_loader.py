import json
from typing import Any, Dict


def load_config(path: str) -> Dict[str, Any]:
    """
    Load a configuration from a JSON file.

    Args:
        path (str): The path to the JSON file to be loaded.

    Returns:
        Dict[str, Any]: A dictionary containing the parsed JSON data.
    """
    with open(path, 'r') as file:
        return json.load(file)
