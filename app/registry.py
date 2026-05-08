from __future__ import annotations

import json
import os
from pathlib import Path

from app.config import load_config


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def get_levels_dir() -> Path:
    return get_project_root() / "levels"


def get_display_language(lang: str | None = None, base_dir: str | Path | None = None) -> str:
    if lang is not None:
        return lang
    env_lang = os.environ.get("NODIST_LANG")
    if env_lang is not None:
        return env_lang
    return load_config(base_dir).get("language", "ja")


def load_level_meta(level_id: str) -> dict | None:
    path = get_levels_dir() / level_id / "meta.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def get_localized_meta_value(
    meta: dict, field_name: str, lang: str | None = None, base_dir: str | Path | None = None
):
    selected_lang = get_display_language(lang, base_dir)
    value = meta.get(field_name)

    if isinstance(value, dict):
        for candidate in (selected_lang, "ja", "en"):
            if candidate in value:
                return value[candidate]
        return next(iter(value.values()), None)

    localized_key = f"{field_name}_{selected_lang}"
    if localized_key in meta:
        return meta[localized_key]

    if selected_lang == "en" and value is not None:
        return value

    for fallback_lang in ("ja", "en"):
        fallback_key = f"{field_name}_{fallback_lang}"
        if fallback_key in meta:
            return meta[fallback_key]
    return value


def sort_key(level: dict) -> int:
    return int(level["id"].split("_")[1])


def list_levels() -> list[dict[str, str]]:
    levels = []
    for level_dir in get_levels_dir().iterdir():
        if not level_dir.is_dir():
            continue
        meta = load_level_meta(level_dir.name)
        if meta is None:
            continue
        levels.append({"id": meta["id"], "title": get_localized_meta_value(meta, "title")})
    return sorted(levels, key=sort_key)


def get_level(level_id: str) -> dict[str, str] | None:
    meta = load_level_meta(level_id)
    if meta is None:
        return None
    return {"id": meta["id"], "title": get_localized_meta_value(meta, "title")}


def get_previous_level(level_id: str) -> str | None:
    meta = load_level_meta(level_id)
    if meta is None:
        return None
    return meta.get("previous_level")


def get_level_hints(
    level_id: str, lang: str | None = None, base_dir: str | Path | None = None
) -> list[str]:
    meta = load_level_meta(level_id)
    if meta is None:
        return []
    hints = get_localized_meta_value(meta, "hints", lang, base_dir)
    return hints or []


def load_localized_asset(
    level_id: str, base_name: str, lang: str | None = None, base_dir: str | Path | None = None
) -> str | None:
    selected_lang = get_display_language(lang, base_dir)
    level_dir = get_levels_dir() / level_id
    candidates = [
        level_dir / f"{base_name}_{selected_lang}.md",
        level_dir / f"{base_name}_ja.md",
        level_dir / f"{base_name}_en.md",
        level_dir / f"{base_name}.md",
    ]
    for path in candidates:
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
    return None


def get_level_task(level_id: str, lang: str | None = None) -> str | None:
    return load_localized_asset(level_id, "task", lang)


def get_level_explanation(level_id: str, lang: str | None = None) -> str | None:
    return load_localized_asset(level_id, "explanation", lang)


def get_level_answer(level_id: str) -> str | None:
    path = get_levels_dir() / level_id / "answer.c"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").rstrip()


def get_level_template(level_id: str) -> str | None:
    path = get_levels_dir() / level_id / "template.c"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def get_level_tests_path(level_id: str) -> Path | None:
    path = get_levels_dir() / level_id / "tests.json"
    if not path.exists():
        return None
    return path
