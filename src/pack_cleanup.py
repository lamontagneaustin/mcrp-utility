"""
pack_cleanup.py — Copy a resource pack and remove junk/hidden files from the copy.

What it removes:
    - Any file or folder whose name starts with '.' (e.g. .DS_Store, .__MACOSX, .git)
    - Common Windows/OS junk files (Thumbs.db, desktop.ini, ehthumbs.db)

The original pack is never modified.
"""

import shutil
from pathlib import Path


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


def remove_junk(pack_root: Path, vlog=None) -> tuple[int, int]:
    """
    Walk pack_root and delete hidden/junk files and folders.
    vlog(msg) is called for each removed item when provided.
    Returns (files_removed, folders_removed).
    """
    files_removed = 0
    folders_removed = 0

    for path in sorted(pack_root.rglob("*"), reverse=True):
        name = path.name
        if not (name.startswith(".") or name.lower() in JUNK_FILENAMES):
            continue

        if path.is_dir():
            shutil.rmtree(path)
            folders_removed += 1
            if vlog:
                vlog(f"  Removed folder: {path.relative_to(pack_root)}")
        elif path.is_file():
            path.unlink()
            files_removed += 1
            if vlog:
                vlog(f"  Removed file:   {path.relative_to(pack_root)}")

    return files_removed, folders_removed
