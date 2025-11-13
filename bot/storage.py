"""Simple JSON-backed storage for bot state."""
import json
from pathlib import Path
from typing import Any

from .config import STATE_FILE

class Storage:
    def __init__(self, path: Path = STATE_FILE):
        self.path = path
        # ensure parent exists
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({})

    def _read(self) -> dict:
        try:
            with self.path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def _write(self, data: dict) -> None:
        with self.path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        data = self._read()
        return data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        data = self._read()
        data[key] = value
        self._write(data)

    def delete(self, key: str) -> None:
        data = self._read()
        if key in data:
            del data[key]
            self._write(data)
