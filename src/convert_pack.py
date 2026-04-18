"""
convert_pack.py — 1.7.10 → 26.1 resource pack conversion logic.

All functions accept an optional vlog(msg) callback for verbose/debug output.
When vlog is None, per-file detail is suppressed.
"""

import json
import shutil
from pathlib import Path

from mappings import (
    ARMOR_RENAMES,
    BLOCK_RENAMES,
    FOLDER_RENAMES,
    ITEM_RENAMES,
    LANG_FORMAT,
    MOB_RENAMES,
    PACK_FORMAT,
)


def rename_folders(pack_root: Path, vlog=None):
    """Rename old folder paths to new ones (e.g. blocks → block)."""
    for old_rel, new_rel in FOLDER_RENAMES.items():
        old_path = pack_root / old_rel
        new_path = pack_root / new_rel
        if old_path.exists() and old_path.is_dir():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            old_path.rename(new_path)
            if vlog:
                vlog(f"  Renamed folder: {old_rel} → {new_rel}")
        else:
            if vlog:
                vlog(f"  (skip) Folder not found: {old_rel}")


def rename_files_in_folder(folder: Path, rename_map: dict, vlog=None) -> tuple[int, int]:
    """
    Rename files in folder according to rename_map {old_basename: new_basename}.
    Returns (renamed_count, not_in_map_count).
    """
    renamed = 0
    not_in_map = 0
    if not folder.exists():
        return 0, 0

    for file in list(folder.iterdir()):
        if not file.is_file():
            continue
        if file.name in rename_map:
            new_name = rename_map[file.name]
            new_path = file.parent / new_name
            if new_path == file:
                if vlog:
                    vlog(f"  (already correct) {file.name}")
            elif new_path.exists():
                file.unlink()
                if vlog:
                    vlog(f"  (skip) {file.name} → {new_name} already exists, dropped duplicate")
            else:
                file.rename(new_path)
                renamed += 1
                if vlog:
                    vlog(f"  Renamed: {file.name} → {new_name}")
        else:
            not_in_map += 1
            if vlog:
                vlog(f"  (not in map) {file.name}")

    return renamed, not_in_map


def rename_entity_textures(entity_root: Path, vlog=None) -> int:
    """Apply MOB_RENAMES inside the entity/ folder."""
    renamed = 0
    if not entity_root.exists():
        return 0
    for old_sub, new_sub in MOB_RENAMES.items():
        old_path = entity_root / old_sub
        new_path = entity_root / new_sub
        if old_path.exists():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            old_path.rename(new_path)
            renamed += 1
            if vlog:
                vlog(f"  Entity: {old_sub} → {new_sub}")
        else:
            if vlog:
                vlog(f"  (skip) Entity not found: {old_sub}")
    return renamed


def rename_armor_textures(pack_root: Path, vlog=None) -> tuple[int, int]:
    """
    Move and rename armor textures from models/armor/ to entity/equipment/.
    Returns (renamed_count, not_found_count).
    """
    textures_root = pack_root / "assets/minecraft/textures"
    renamed = 0
    not_found = 0
    for old_rel, new_rel in ARMOR_RENAMES.items():
        old_path = textures_root / old_rel
        new_path = textures_root / new_rel
        if old_path.exists():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            old_path.rename(new_path)
            renamed += 1
            if vlog:
                vlog(f"  Armor: {old_rel} → {new_rel}")
        else:
            not_found += 1
            if vlog:
                vlog(f"  (skip) Armor not found: {old_rel}")
    return renamed, not_found


def convert_lang_files(pack_root: Path, vlog=None) -> int:
    """Convert .lang files to .json format."""
    lang_folder = pack_root / LANG_FORMAT["folder"]
    if not lang_folder.exists():
        return 0

    converted = 0
    for lang_file in list(lang_folder.glob("*.lang")):
        data = {}
        for line in lang_file.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                data[key.strip()] = value.strip()

        json_path = lang_file.with_suffix(".json")
        json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        lang_file.unlink()
        converted += 1
        if vlog:
            vlog(f"  Lang: {lang_file.name} → {json_path.name}")

    return converted


def update_pack_mcmeta(pack_root: Path, vlog=None):
    """Update pack_format in pack.mcmeta."""
    mcmeta_path = pack_root / "pack.mcmeta"
    if not mcmeta_path.exists():
        mcmeta = {"pack": {"pack_format": PACK_FORMAT, "description": "Converted resource pack"}}
        mcmeta_path.write_text(json.dumps(mcmeta, indent=2), encoding="utf-8")
        if vlog:
            vlog(f"  pack.mcmeta: created with pack_format {PACK_FORMAT}")
        return

    try:
        mcmeta = json.loads(mcmeta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        if vlog:
            vlog("  WARNING: Could not parse pack.mcmeta — skipping update")
        return

    old_format = mcmeta.get("pack", {}).get("pack_format", "?")
    mcmeta.setdefault("pack", {})["pack_format"] = PACK_FORMAT
    mcmeta_path.write_text(json.dumps(mcmeta, indent=2), encoding="utf-8")
    if vlog:
        vlog(f"  pack.mcmeta: pack_format {old_format} → {PACK_FORMAT}")
