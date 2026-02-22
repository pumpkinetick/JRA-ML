import json
from pathlib import Path
from typing import Any

from src import PROJECT_PATH


def load_from_json(file_path: Path) -> Any:
    with open(PROJECT_PATH / file_path) as f:
        return json.load(f)
