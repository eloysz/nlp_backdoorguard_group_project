import json
from pathlib import Path
from typing import Dict, List


def load_json(path: str) -> List[Dict]:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def load_jsonl(path: str) -> List[Dict]:
    rows = []
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows
