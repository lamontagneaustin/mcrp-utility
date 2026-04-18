"""
Minecraft Texture Pack Comparator
Finds texture packs with the same name across two top-level folders,
then compares each matched pair for files that share a name but differ in content.

Usage: python compare_packs.py <folderA> <folderB>
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


def compare_pack_pair(pack1: Path, pack2: Path):
    files1 = get_relative_files(pack1)
    files2 = get_relative_files(pack2)

    shared    = set(files1.keys()) & set(files2.keys())
    only_in_1 = set(files1.keys()) - set(files2.keys())
    only_in_2 = set(files2.keys()) - set(files1.keys())

    identical = []
    different = []

    for rel in sorted(shared):
        h1 = file_hash(files1[rel])
        h2 = file_hash(files2[rel])
        if h1 == h2:
            identical.append(rel)
        else:
            different.append(rel)

    return dict(
        identical=identical,
        different=different,
        only_in_1=sorted(only_in_1),
        only_in_2=sorted(only_in_2),
    )


def compare_folders(folder_a: Path, folder_b: Path):
    packs_a = {p.name: p for p in folder_a.iterdir() if p.is_dir()}
    packs_b = {p.name: p for p in folder_b.iterdir() if p.is_dir()}

    matched   = sorted(set(packs_a.keys()) & set(packs_b.keys()))
    only_in_a = sorted(set(packs_a.keys()) - set(packs_b.keys()))
    only_in_b = sorted(set(packs_b.keys()) - set(packs_a.keys()))

    print(f"\n{'='*60}")
    print(f"  TOP-LEVEL FOLDER SUMMARY")
    print(f"{'='*60}")
    print(f"  Folder A: {folder_a}")
    print(f"  Folder B: {folder_b}")
    print(f"  Matched packs:       {len(matched)}")
    print(f"  Only in Folder A:    {len(only_in_a)}")
    print(f"  Only in Folder B:    {len(only_in_b)}")
    print(f"{'='*60}")

    if only_in_a:
        print(f"\n📁 Packs only in Folder A:")
        for name in only_in_a:
            print(f"  -  {name}")

    if only_in_b:
        print(f"\n📁 Packs only in Folder B:")
        for name in only_in_b:
            print(f"  -  {name}")

    if not matched:
        print("\nNo matching pack names found between the two folders.")
        return

    total_different = 0

    for pack_name in matched:
        pack1 = packs_a[pack_name]
        pack2 = packs_b[pack_name]
        result = compare_pack_pair(pack1, pack2)

        total_files = len(result["identical"]) + len(result["different"])
        has_issues = result["different"] or result["only_in_1"] or result["only_in_2"]
        total_different += len(result["different"])

        print(f"\n{'─'*60}")
        print(f"  📦 {pack_name}")
        print(f"{'─'*60}")
        print(f"  Shared files:   {total_files}  |  "
              f"Identical: {len(result['identical'])}  |  "
              f"Different: {len(result['different'])}")
        print(f"  Only in A: {len(result['only_in_1'])}  |  Only in B: {len(result['only_in_2'])}")

        if result["different"]:
            print(f"\n  ⚠️  Same name, different content:")
            for rel in result["different"]:
                print(f"    ✗  {rel}")

        if result["only_in_1"]:
            print(f"\n  📄 Only in Folder A:")
            for rel in result["only_in_1"]:
                print(f"    -  {rel}")

        if result["only_in_2"]:
            print(f"\n  📄 Only in Folder B:")
            for rel in result["only_in_2"]:
                print(f"    -  {rel}")

        if not has_issues:
            print(f"\n  ✅ All files are identical!")

    print(f"\n{'='*60}")
    print(f"  TOTAL mismatched files across all packs: {total_different}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_packs.py <folderA> <folderB>")
        sys.exit(1)

    folder_a = Path(sys.argv[1])
    folder_b = Path(sys.argv[2])

    if not folder_a.is_dir():
        print(f"Error: '{folder_a}' is not a valid directory.")
        sys.exit(1)
    if not folder_b.is_dir():
        print(f"Error: '{folder_b}' is not a valid directory.")
        sys.exit(1)

    compare_folders(folder_a, folder_b)