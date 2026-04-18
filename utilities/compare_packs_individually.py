"""
Minecraft Texture Pack Comparator
Compares two texture packs and prints files that share a name but differ in content.
Usage: python compare_packs.py <pack1_folder> <pack2_folder>
"""

import hashlib
import sys
from pathlib import Path


def file_hash(path: Path) -> str:
    """Return the MD5 hash of a file's contents."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_relative_files(folder: Path) -> dict[str, Path]:
    """Return a dict of {relative_path_str: absolute_path} for all files in a folder."""
    return {
        str(p.relative_to(folder)): p
        for p in folder.rglob("*")
        if p.is_file()
    }


def compare_packs(pack1: Path, pack2: Path):
    print(f"\nPack 1: {pack1}")
    print(f"Pack 2: {pack2}")
    print("-" * 60)

    files1 = get_relative_files(pack1)
    files2 = get_relative_files(pack2)

    shared = set(files1.keys()) & set(files2.keys())
    only_in_1 = set(files1.keys()) - set(files2.keys())
    only_in_2 = set(files2.keys()) - set(files1.keys())

    # Compare shared files
    identical = []
    different = []

    for rel in sorted(shared):
        h1 = file_hash(files1[rel])
        h2 = file_hash(files2[rel])
        if h1 == h2:
            identical.append(rel)
        else:
            different.append(rel)

    # --- Report ---
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Shared files:      {len(shared)}")
    print(f"  Identical:         {len(identical)}")
    print(f"  DIFFERENT:         {len(different)}")
    print(f"  Only in Pack 1:    {len(only_in_1)}")
    print(f"  Only in Pack 2:    {len(only_in_2)}")
    print(f"{'='*60}")

    if different:
        print(f"\n⚠️  FILES WITH SAME NAME BUT DIFFERENT CONTENT ({len(different)}):")
        for rel in different:
            print(f"  ✗  {rel}")
    else:
        print("\n✅ All shared files are identical!")

    if only_in_1:
        print(f"\n📁 Only in Pack 1 ({len(only_in_1)}):")
        for rel in sorted(only_in_1):
            print(f"  -  {rel}")

    if only_in_2:
        print(f"\n📁 Only in Pack 2 ({len(only_in_2)}):")
        for rel in sorted(only_in_2):
            print(f"  -  {rel}")

    print()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_packs.py <pack1_folder> <pack2_folder>")
        sys.exit(1)

    pack1 = Path(sys.argv[1])
    pack2 = Path(sys.argv[2])

    if not pack1.is_dir():
        print(f"Error: '{pack1}' is not a valid directory.")
        sys.exit(1)
    if not pack2.is_dir():
        print(f"Error: '{pack2}' is not a valid directory.")
        sys.exit(1)

    compare_packs(pack1, pack2)