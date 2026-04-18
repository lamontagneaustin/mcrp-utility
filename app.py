"""
app.py — GUI entry point for the Minecraft resource pack converter.

Runs the full pipeline:
  1. Copy the input pack to output_folder/new_name
  2. Remove junk/hidden files from the copy
  3. Convert the copy from 1.7.10 format to modern format (26.1)
"""

import sys
import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, scrolledtext
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from pack_cleanup import copy_pack, remove_junk
from convert_pack import (
    rename_folders,
    rename_files_in_folder,
    rename_entity_textures,
    rename_armor_textures,
    convert_lang_files,
    update_pack_mcmeta,
)
from mappings import BLOCK_RENAMES, ITEM_RENAMES

LOGS_DIR = Path(__file__).parent / "output"


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline(input_path: Path, output_path: Path, log, vlog):
    """
    Copy, clean, and convert the pack.
    log  — always shown in the GUI
    vlog — only shown when debug mode is on (per-file detail)
    """
    try:
        log("=" * 56)
        log(f"  Input:  {input_path}")
        log(f"  Output: {output_path}")
        log("=" * 56)

        # Step 1 — copy
        log("\n[1/9] Copying pack...")
        copy_pack(input_path, output_path)
        log(f"  Copied to {output_path}")

        # Step 2 — clean junk
        log("\n[2/9] Removing junk files...")
        files, folders = remove_junk(output_path, vlog=vlog)
        log(f"  Removed: {files} file(s), {folders} folder(s)")

        # Step 3 — rename folders
        log("\n[3/9] Renaming folders...")
        rename_folders(output_path, vlog=vlog)

        # Step 4 — rename block textures
        block_folder = output_path / "assets/minecraft/textures/block"
        log("\n[4/9] Renaming block textures...")
        renamed, not_in_map = rename_files_in_folder(block_folder, BLOCK_RENAMES, vlog=vlog)
        log(f"  Renamed: {renamed}  |  Not in map: {not_in_map}")

        # Step 5 — rename item textures
        item_folder = output_path / "assets/minecraft/textures/item"
        log("\n[5/9] Renaming item textures...")
        renamed, not_in_map = rename_files_in_folder(item_folder, ITEM_RENAMES, vlog=vlog)
        log(f"  Renamed: {renamed}  |  Not in map: {not_in_map}")

        # Step 6 — rename entity textures
        entity_folder = output_path / "assets/minecraft/textures/entity"
        log("\n[6/9] Renaming entity textures...")
        count = rename_entity_textures(entity_folder, vlog=vlog)
        log(f"  Renamed: {count}")

        # Step 7 — move armor textures
        log("\n[7/9] Moving armor textures (models/armor → entity/equipment)...")
        renamed, not_found = rename_armor_textures(output_path, vlog=vlog)
        log(f"  Moved: {renamed}  |  Not found: {not_found}")

        # Step 8 — convert .lang → .json
        log("\n[8/9] Converting language files...")
        count = convert_lang_files(output_path, vlog=vlog)
        log(f"  Converted: {count} .lang file(s)")

        # Step 9 — update pack.mcmeta
        log("\n[9/9] Updating pack.mcmeta...")
        update_pack_mcmeta(output_path, vlog=log)

        log(f"\n  Done! Output: {output_path}")
        log("=" * 56 + "\n")
        return True

    except (FileExistsError, ValueError) as e:
        log(f"\n  ERROR: {e}\n")
        return False
    except Exception as e:
        log(f"\n  UNEXPECTED ERROR: {e}\n")
        return False


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minecraft Pack Converter")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        # ── Input pack ──────────────────────────────────────────────────────
        tk.Label(self, text="Input pack:", anchor="w").grid(
            row=0, column=0, sticky="w", **pad)
        self.input_var = tk.StringVar()
        self.input_var.trace_add("write", self._on_input_changed)
        tk.Entry(self, textvariable=self.input_var, width=48).grid(
            row=0, column=1, **pad)
        tk.Button(self, text="Browse…", command=self._browse_input).grid(
            row=0, column=2, padx=(0, 10))

        # ── Output folder ───────────────────────────────────────────────────
        tk.Label(self, text="Output folder:", anchor="w").grid(
            row=1, column=0, sticky="w", **pad)
        self.output_var = tk.StringVar()
        tk.Entry(self, textvariable=self.output_var, width=48).grid(
            row=1, column=1, **pad)
        tk.Button(self, text="Browse…", command=self._browse_output).grid(
            row=1, column=2, padx=(0, 10))

        # ── New name ─────────────────────────────────────────────────────────
        tk.Label(self, text="New pack name:", anchor="w").grid(
            row=2, column=0, sticky="w", **pad)
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var, width=48).grid(
            row=2, column=1, **pad)

        # ── Go button ────────────────────────────────────────────────────────
        self.go_btn = tk.Button(
            self, text="Go", width=16,
            bg="#4CAF50", fg="white", font=("", 11, "bold"),
            command=self._on_go,
        )
        self.go_btn.grid(row=3, column=0, columnspan=3, pady=(4, 10))

        # ── Log area ─────────────────────────────────────────────────────────
        self.log_box = scrolledtext.ScrolledText(
            self, width=70, height=22,
            state="disabled", bg="#1e1e1e", fg="#d4d4d4",
            font=("Consolas", 9), wrap="word",
        )
        self.log_box.grid(row=4, column=0, columnspan=3, padx=10, pady=(0, 10))

    # ── Callbacks ────────────────────────────────────────────────────────────

    def _browse_input(self):
        folder = filedialog.askdirectory(title="Select input pack folder")
        if folder:
            self.input_var.set(folder)

    def _browse_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_var.set(folder)

    def _on_input_changed(self, *_):
        raw = self.input_var.get().strip()
        if raw:
            self.name_var.set(f"updated_{Path(raw).name}")

    def _on_go(self):
        input_str  = self.input_var.get().strip()
        output_str = self.output_var.get().strip()
        name_str   = self.name_var.get().strip()

        if not input_str:
            self._log("ERROR: Please select an input pack folder.\n")
            return
        if not output_str:
            self._log("ERROR: Please select an output folder.\n")
            return
        if not name_str:
            self._log("ERROR: Please enter a name for the converted pack.\n")
            return

        input_path  = Path(input_str)
        output_path = Path(output_str) / name_str

        if not input_path.exists():
            self._log(f"ERROR: Input folder does not exist:\n  {input_path}\n")
            return

        self._clear_log()
        self.go_btn.config(state="disabled", text="Working…")
        threading.Thread(
            target=self._run,
            args=(input_path, output_path),
            daemon=True,
        ).start()

    def _run(self, input_path: Path, output_path: Path):
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = LOGS_DIR / f"{timestamp}.log"

        with log_file.open("w", encoding="utf-8") as f:
            def log(message: str):
                f.write(message + "\n")
                f.flush()
                self._log(message)

            def vlog(message: str):
                f.write(message + "\n")
                f.flush()

            run_pipeline(input_path, output_path, log, vlog)

        self.after(0, lambda: self.go_btn.config(state="normal", text="Go"))

    # ── Log helpers ──────────────────────────────────────────────────────────

    def _log(self, message: str):
        def _write():
            self.log_box.config(state="normal")
            self.log_box.insert("end", message + "\n")
            self.log_box.see("end")
            self.log_box.config(state="disabled")
        self.after(0, _write)

    def _clear_log(self):
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()
