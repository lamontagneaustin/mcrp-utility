# Minecraft Texture Pack Converter

Converts Minecraft resource packs from **1.7.10** to **26.1** (pack format 101.1).

## Usage

Run `app.py` to open the GUI:

```
python app.py
```

1. Select the input pack folder
2. Select where to save the output
3. Set a name for the converted pack
4. Click **Go**

The original pack is never modified. Conversion logs are saved to `./output/`.

## What it does

- Copies the pack and removes hidden/junk files
- Renames `textures/blocks` → `textures/block` and `textures/items` → `textures/item`
- Renames block, item, entity, and armor textures to match modern naming
- Moves armor textures from `models/armor/` to `entity/equipment/humanoid/`
- Converts `.lang` files to `.json`
- Updates `pack_format` in `pack.mcmeta`

## Files

| File | Purpose |
|------|---------|
| `app.py` | GUI entry point |
| `convert_pack.py` | Conversion logic |
| `pack_cleanup.py` | Copy and junk file removal |
| `mappings.py` | All rename/move mappings |
