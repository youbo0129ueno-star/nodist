from __future__ import annotations

import json
import os
from pathlib import Path


DEFAULT_LANGUAGE = "ja"


def get_config_path(base_dir: str | Path | None = None) -> Path:
    if base_dir is not None:
        base = Path(base_dir)
    else:
        base = Path(os.environ.get("NODIST_HOME", Path.home()))
    return base / ".nodist" / "config.json"


def load_config(base_dir: str | Path | None = None) -> dict[str, str]:
    path = get_config_path(base_dir)
    if not path.exists():
        return {"language": DEFAULT_LANGUAGE}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"language": DEFAULT_LANGUAGE}

    language = data.get("language", DEFAULT_LANGUAGE)
    if language not in {"ja", "en"}:
        language = DEFAULT_LANGUAGE
    return {"language": language}


def save_config(config: dict[str, str], base_dir: str | Path | None = None) -> dict[str, str]:
    path = get_config_path(base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = {"language": config.get("language", DEFAULT_LANGUAGE)}
    path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    return normalized


def set_language(language: str, base_dir: str | Path | None = None) -> dict[str, str]:
    return save_config({"language": language}, base_dir)
