

"""
config.py

Loads and validates the unified modeling configuration for the UEVF-ASCDE pipeline.
"""

import json
import os

def load_modeling_config(path: str) -> dict:
    """
    Load and return the unified modeling configuration from a JSON file.

    Parameters:
    - path: Path to the JSON config file.

    Returns:
    - config: A dictionary containing all modeling parameters.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with open(path, 'r') as f:
        config = json.load(f)
    return config