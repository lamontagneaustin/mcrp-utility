"""
convert_pack.py — Convert a 1.7.10 Minecraft resource pack to modern format (26.1 / pack format 46)

Usage:
    python src/convert_pack.py <input_pack_folder> [output_folder]

What it does:
    1. Copies the entire pack to the output folder
    2. Renames textures/blocks → textures/block and textures/items → textures/item
    3. Renames individual block/item files using the mappings table
    4. Renames entity/mob textures
    5. Converts .lang files to .json format
    6. Updates pack.mcmeta with the new pack_format number

Requires no external libraries — uses only Python stdlib.
"""

import json
import re
import shutil
import sys
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def copy_pack(src: Path, dst: Path):
    if src.resolve() == dst.resolve():
        raise ValueError(f"Input and output are the same path: {src}")
    if dst.exists():
        raise FileExistsError(f"Output folder already exists: '{dst}'\nDelete or rename it, then run again.")
    shutil.copytree(src, dst)
    print(f"  Copied pack to {dst}")


def rename_folders(pack_root: Path) -> dict[str, int]:
    """Rename old folder paths to new ones. Returns counts."""
    counts = {}
    for old_rel, new_rel in FOLDER_RENAMES.items():
        old_path = pack_root / old_rel
        new_path = pack_root / new_rel
        if old_path.exists() and old_path.is_dir():
            new_path.parent.mkdir(parents=True, exist_ok=True)
            old_path.rename(new_path)
            counts[f"{old_rel} → {new_rel}"] = 1
            print(f"  Renamed folder: {old_rel} → {new_rel}")
        else:
            print(f"  (skip) Folder not found: {old_rel}")
    return counts


def rename_files_in_folder(folder: Path, rename_map: dict) -> tuple[int, int]:
    """
    Rename files in a folder according to rename_map {old_basename: new_basename}.
    Returns (renamed_count, not_found_count).
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
                pass  # already the right name
            elif new_path.exists():
                print(f"  (skip) {file.name} → {new_name} already exists, dropping duplicate")
                file.unlink()
            else:
                file.rename(new_path)
                renamed += 1
        else:
            not_in_map += 1

    return renamed, not_in_map


def rename_entity_textures(entity_root: Path) -> int:
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
            print(f"  Entity: {old_sub} → {new_sub}")
        else:
            print(f"  (skip) Entity not found: {old_sub}")
    return renamed


def rename_armor_textures(pack_root: Path) -> tuple[int, int]:
    """
    Move and rename armor textures from models/armor/ to entity/equipment/.
    Paths in ARMOR_RENAMES are relative to assets/minecraft/textures/.
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
            print(f"  Armor: {old_rel} → {new_rel}")
        else:
            not_found += 1
            print(f"  (skip) Armor not found: {old_rel}")
    return renamed, not_found


def convert_lang_files(pack_root: Path) -> int:
    """Convert .lang files to .json format."""
    lang_folder = pack_root / LANG_FORMAT["folder"]
    if not lang_folder.exists():
        return 0

    converted = 0
    for lang_file in list(lang_folder.glob("*.lang")):
        data = {}
        lines = lang_file.read_text(encoding="utf-8", errors="replace").splitlines()
        for line in lines:
            line = line.strip()
            # Skip comments and blank lines
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                data[key.strip()] = value.strip()

        json_path = lang_file.with_suffix(".json")
        json_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        lang_file.unlink()
        converted += 1
        print(f"  Lang: {lang_file.name} → {json_path.name}")

    return converted


def update_pack_mcmeta(pack_root: Path):
    """Update pack_format in pack.mcmeta."""
    mcmeta_path = pack_root / "pack.mcmeta"
    if not mcmeta_path.exists():
        # Create a minimal one if missing
        mcmeta = {
            "pack": {
                "pack_format": PACK_FORMAT,
                "description": "Converted resource pack"
            }
        }
        mcmeta_path.write_text(json.dumps(mcmeta, indent=2), encoding="utf-8")
        print(f"  pack.mcmeta: created with pack_format {PACK_FORMAT}")
        return

    try:
        mcmeta = json.loads(mcmeta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("  WARNING: Could not parse pack.mcmeta — skipping update")
        return

    old_format = mcmeta.get("pack", {}).get("pack_format", "?")
    mcmeta.setdefault("pack", {})["pack_format"] = PACK_FORMAT
    mcmeta_path.write_text(json.dumps(mcmeta, indent=2), encoding="utf-8")
    print(f"  pack.mcmeta: pack_format {old_format} → {PACK_FORMAT}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def convert_pack(input_path: Path, output_path: Path):
    print(f"\n{'='*60}")
    print(f"  Converting: {input_path.name}")
    print(f"{'='*60}")

    # Step 1 — copy
    print("\n[1/6] Copying pack...")
    copy_pack(input_path, output_path)

    # Step 2 — rename folders
    print("\n[2/6] Renaming folders...")
    rename_folders(output_path)

    # Step 3 — rename block textures
    block_folder = output_path / "assets/minecraft/textures/block"
    print(f"\n[3/6] Renaming block textures in {block_folder.relative_to(output_path)}...")
    renamed, unchanged = rename_files_in_folder(block_folder, BLOCK_RENAMES)
    print(f"  Renamed: {renamed}  |  Already correct / not in map: {unchanged}")

    # Step 4 — rename item textures
    item_folder = output_path / "assets/minecraft/textures/item"
    print(f"\n[4/6] Renaming item textures in {item_folder.relative_to(output_path)}...")
    renamed, unchanged = rename_files_in_folder(item_folder, ITEM_RENAMES)
    print(f"  Renamed: {renamed}  |  Already correct / not in map: {unchanged}")

    # Step 5 — rename entity textures
    entity_folder = output_path / "assets/minecraft/textures/entity"
    print("\n[5/6] Renaming entity textures...")
    count = rename_entity_textures(entity_folder)
    print(f"  Renamed: {count}")

    # Step 6 — move and rename armor textures
    print("\n[6/7] Moving armor textures (models/armor → entity/equipment)...")
    renamed, not_found = rename_armor_textures(output_path)
    print(f"  Moved: {renamed}  |  Not found: {not_found}")

    # Step 7 — convert .lang → .json
    print("\n[7/7] Converting language files...")
    count = convert_lang_files(output_path)
    print(f"  Converted: {count} .lang file(s)")

    # Step 7 — update pack.mcmeta
    print("\n[+] Updating pack.mcmeta...")
    update_pack_mcmeta(output_path)

    print(f"\n✅ Done! Output: {output_path}\n")


def convert_folder_of_packs(input_folder: Path, output_folder: Path):
    """Convert every subdirectory in input_folder as its own pack."""
    packs = [p for p in input_folder.iterdir() if p.is_dir()]
    if not packs:
        print(f"No subdirectories found in {input_folder}")
        return

    output_folder.mkdir(parents=True, exist_ok=True)
    print(f"\nFound {len(packs)} pack(s) to convert.")

    for pack in sorted(packs):
        out = output_folder / pack.name
        convert_pack(pack, out)

    print(f"\n{'='*60}")
    print(f"  All done! {len(packs)} pack(s) converted.")
    print(f"  Output folder: {output_folder}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python convert_pack.py <input_folder> [output_folder]")
        print("")
        print("  input_folder  — either a single pack, or a folder containing multiple packs")
        print("  output_folder — where to write the converted pack (optional)")
        print("                  defaults to 'updated_<input_name>' next to the input")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: '{input_path}' does not exist.")
        sys.exit(1)

    if len(sys.argv) == 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.parent / f"updated_{input_path.name}"

    # Auto-detect: if the input contains pack.mcmeta it's a single pack,
    # otherwise treat it as a folder of packs.
    if (input_path / "pack.mcmeta").exists():
        convert_pack(input_path, output_path)
    else:
        convert_folder_of_packs(input_path, output_path)
