"""
pack_cleanup.py — Copy a Minecraft resource pack and remove junk/hidden files from the copy.

Usage:
    python pack_cleanup.py <input_pack_folder> [output_folder]

What it removes:
    - Any file or folder whose name starts with '.' (e.g. .DS_Store, .__MACOSX, .git)
    - Common Windows/OS junk files (Thumbs.db, desktop.ini, ehthumbs.db)

The original pack is never modified.
"""

import shutil
import sys
from pathlib import Path


# Files to remove regardless of whether they start with '.'
JUNK_FILENAMES = {
    "thumbs.db",
    "desktop.ini",
    "ehthumbs.db",
}


def copy_pack(src: Path, dst: Path):
    if src.resolve() == dst.resolve():
        raise ValueError(f"Input and output are the same path: {src}")
    if dst.exists():
        raise FileExistsError(
            f"Output folder already exists: '{dst}'\n"
            f"Delete or rename it, then run again."
        )
    shutil.copytree(src, dst)
    print(f"  Copied pack to {dst}")


def remove_junk(pack_root: Path) -> tuple[int, int]:
    """
    Walk pack_root and delete hidden/junk files and folders.
    Returns (files_removed, folders_removed).
    """
    files_removed = 0
    folders_removed = 0

    # Walk bottom-up so we can safely delete folders
    for path in sorted(pack_root.rglob("*"), reverse=True):
        name = path.name

        is_hidden = name.startswith(".")
        is_junk = name.lower() in JUNK_FILENAMES

        if not (is_hidden or is_junk):
            continue

        if path.is_dir():
            shutil.rmtree(path)
            folders_removed += 1
            print(f"  Removed folder: {path.relative_to(pack_root)}")
        elif path.is_file():
            path.unlink()
            files_removed += 1
            print(f"  Removed file:   {path.relative_to(pack_root)}")

    return files_removed, folders_removed


def cleanup_pack(input_path: Path, output_path: Path):
    print(f"\n{'='*60}")
    print(f"  Cleaning: {input_path.name}")
    print(f"{'='*60}")

    print("\n[1/2] Copying pack...")
    copy_pack(input_path, output_path)

    print("\n[2/2] Removing junk files...")
    files, folders = remove_junk(output_path)
    print(f"  Removed: {files} file(s), {folders} folder(s)")

    print(f"\nDone! Output: {output_path}\n")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python pack_cleanup.py <input_folder> [output_folder]")
        print("")
        print("  input_folder  — the pack to clean up")
        print("  output_folder — where to write the cleaned copy (optional)")
        print("                  defaults to 'cleaned_<input_name>' next to the input")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: '{input_path}' does not exist.")
        sys.exit(1)

    if len(sys.argv) == 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.parent / f"cleaned_{input_path.name}"

    cleanup_pack(input_path, output_path)
