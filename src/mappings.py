"""
mappings.py — 1.7.10 → Modern Minecraft (26.1 / pack format 46) conversion mappings.

Since packs already have individually named files (not terrain.png/items.png atlases),
this file only needs:
  - PACK_FORMAT:    the pack_format number for pack.mcmeta
  - FOLDER_RENAMES: old folder prefix → new folder prefix
  - FILE_RENAMES:   old filename (just the basename, no folder) → new filename
                    Applied AFTER folder renames, so use the new folder context.
                    Keys are old basenames; values are new basenames.
                    Files not listed here keep their existing name, just moved
                    to the renamed folder.
  - MOB_RENAMES:    entity texture files that moved or were renamed
  - LANG_FORMAT:    how to handle language files
"""

# ---------------------------------------------------------------------------
# Pack format for pack.mcmeta (26.1 = format 84.0)
# ---------------------------------------------------------------------------
PACK_FORMAT = 84.0

# ---------------------------------------------------------------------------
# Folder renames — swap these path prefixes across the whole pack
# ---------------------------------------------------------------------------
FOLDER_RENAMES = {
    "assets/minecraft/textures/blocks": "assets/minecraft/textures/block",
    "assets/minecraft/textures/items":  "assets/minecraft/textures/item",
}

# ---------------------------------------------------------------------------
# Block texture file renames (basenames only)
# Old name → new name. Applied inside textures/block/ after folder rename.
# Files not listed here are kept as-is (name was unchanged between versions).
# ---------------------------------------------------------------------------
BLOCK_RENAMES = {
    # Flowers
    "flower_rose.png":               "poppy.png",
    "flower_dandelion.png":          "dandelion.png",

    # Leaves
    "leaves_oak.png":                "oak_leaves.png",
    "leaves_spruce.png":             "spruce_leaves.png",
    "leaves_birch.png":              "birch_leaves.png",
    "leaves_jungle.png":             "jungle_leaves.png",
    "leaves_oak_opaque.png":         "oak_leaves.png",       # MCPatcher opaque variant
    "leaves_spruce_opaque.png":      "spruce_leaves.png",
    "leaves_birch_opaque.png":       "birch_leaves.png",
    "leaves_jungle_opaque.png":      "jungle_leaves.png",

    # Logs
    "log_oak.png":                   "oak_log.png",
    "log_spruce.png":                "spruce_log.png",
    "log_birch.png":                 "birch_log.png",
    "log_jungle.png":                "jungle_log.png",
    "log_oak_top.png":               "oak_log_top.png",
    "log_spruce_top.png":            "spruce_log_top.png",
    "log_birch_top.png":             "birch_log_top.png",
    "log_jungle_top.png":            "jungle_log_top.png",

    # Planks
    "planks_oak.png":                "oak_planks.png",
    "planks_spruce.png":             "spruce_planks.png",
    "planks_birch.png":              "birch_planks.png",
    "planks_jungle.png":             "jungle_planks.png",
    "planks_acacia.png":             "acacia_planks.png",
    "planks_big_oak.png":            "dark_oak_planks.png",

    # Saplings
    "sapling_oak.png":               "oak_sapling.png",
    "sapling_spruce.png":            "spruce_sapling.png",
    "sapling_birch.png":             "birch_sapling.png",
    "sapling_jungle.png":            "jungle_sapling.png",
    "sapling_acacia.png":            "acacia_sapling.png",
    "sapling_roofed_oak.png":        "dark_oak_sapling.png",

    # Stone variants
    "stonebrick.png":                "stone_bricks.png",
    "stonebrick_mossy.png":          "mossy_stone_bricks.png",
    "stonebrick_cracked.png":        "cracked_stone_bricks.png",
    "stonebrick_carved.png":         "chiseled_stone_bricks.png",
    "cobblestone_mossy.png":         "mossy_cobblestone.png",

    # Sandstone
    "sandstone_carved.png":          "chiseled_sandstone.png",
    "sandstone_smooth.png":          "cut_sandstone.png",
    "sandstone_top.png":             "sandstone_top.png",    # unchanged
    "sandstone_bottom.png":          "sandstone_bottom.png", # unchanged
    "sandstone_normal.png":          "sandstone.png",

    # Red sandstone (added in 1.8)
    "red_sandstone_carved.png":      "chiseled_red_sandstone.png",
    "red_sandstone_smooth.png":      "cut_red_sandstone.png",
    "red_sandstone_top.png":         "red_sandstone_top.png",
    "red_sandstone_bottom.png":      "red_sandstone_bottom.png",
    "red_sandstone_normal.png":      "red_sandstone.png",

    # Wool
    "wool_colored_white.png":        "white_wool.png",
    "wool_colored_orange.png":       "orange_wool.png",
    "wool_colored_magenta.png":      "magenta_wool.png",
    "wool_colored_light_blue.png":   "light_blue_wool.png",
    "wool_colored_yellow.png":       "yellow_wool.png",
    "wool_colored_lime.png":         "lime_wool.png",
    "wool_colored_pink.png":         "pink_wool.png",
    "wool_colored_gray.png":         "gray_wool.png",
    "wool_colored_silver.png":       "light_gray_wool.png",
    "wool_colored_cyan.png":         "cyan_wool.png",
    "wool_colored_purple.png":       "purple_wool.png",
    "wool_colored_blue.png":         "blue_wool.png",
    "wool_colored_brown.png":        "brown_wool.png",
    "wool_colored_green.png":        "green_wool.png",
    "wool_colored_red.png":          "red_wool.png",
    "wool_colored_black.png":        "black_wool.png",

    # Stained glass
    "glass_white.png":               "white_stained_glass.png",
    "glass_orange.png":              "orange_stained_glass.png",
    "glass_magenta.png":             "magenta_stained_glass.png",
    "glass_light_blue.png":          "light_blue_stained_glass.png",
    "glass_yellow.png":              "yellow_stained_glass.png",
    "glass_lime.png":                "lime_stained_glass.png",
    "glass_pink.png":                "pink_stained_glass.png",
    "glass_gray.png":                "gray_stained_glass.png",
    "glass_silver.png":              "light_gray_stained_glass.png",
    "glass_cyan.png":                "cyan_stained_glass.png",
    "glass_purple.png":              "purple_stained_glass.png",
    "glass_blue.png":                "blue_stained_glass.png",
    "glass_brown.png":               "brown_stained_glass.png",
    "glass_green.png":               "green_stained_glass.png",
    "glass_red.png":                 "red_stained_glass.png",
    "glass_black.png":               "black_stained_glass.png",

    # Stained glass pane tops (same pattern)
    "glass_pane_top_white.png":      "white_stained_glass_pane_top.png",
    "glass_pane_top_orange.png":     "orange_stained_glass_pane_top.png",
    "glass_pane_top_magenta.png":    "magenta_stained_glass_pane_top.png",
    "glass_pane_top_light_blue.png": "light_blue_stained_glass_pane_top.png",
    "glass_pane_top_yellow.png":     "yellow_stained_glass_pane_top.png",
    "glass_pane_top_lime.png":       "lime_stained_glass_pane_top.png",
    "glass_pane_top_pink.png":       "pink_stained_glass_pane_top.png",
    "glass_pane_top_gray.png":       "gray_stained_glass_pane_top.png",
    "glass_pane_top_silver.png":     "light_gray_stained_glass_pane_top.png",
    "glass_pane_top_cyan.png":       "cyan_stained_glass_pane_top.png",
    "glass_pane_top_purple.png":     "purple_stained_glass_pane_top.png",
    "glass_pane_top_blue.png":       "blue_stained_glass_pane_top.png",
    "glass_pane_top_brown.png":      "brown_stained_glass_pane_top.png",
    "glass_pane_top_green.png":      "green_stained_glass_pane_top.png",
    "glass_pane_top_red.png":        "red_stained_glass_pane_top.png",
    "glass_pane_top_black.png":      "black_stained_glass_pane_top.png",

    # Hardened clay (terracotta)
    "hardened_clay_stained_white.png":      "white_terracotta.png",
    "hardened_clay_stained_orange.png":     "orange_terracotta.png",
    "hardened_clay_stained_magenta.png":    "magenta_terracotta.png",
    "hardened_clay_stained_light_blue.png": "light_blue_terracotta.png",
    "hardened_clay_stained_yellow.png":     "yellow_terracotta.png",
    "hardened_clay_stained_lime.png":       "lime_terracotta.png",
    "hardened_clay_stained_pink.png":       "pink_terracotta.png",
    "hardened_clay_stained_gray.png":       "gray_terracotta.png",
    "hardened_clay_stained_silver.png":     "light_gray_terracotta.png",
    "hardened_clay_stained_cyan.png":       "cyan_terracotta.png",
    "hardened_clay_stained_purple.png":     "purple_terracotta.png",
    "hardened_clay_stained_blue.png":       "blue_terracotta.png",
    "hardened_clay_stained_brown.png":      "brown_terracotta.png",
    "hardened_clay_stained_green.png":      "green_terracotta.png",
    "hardened_clay_stained_red.png":        "red_terracotta.png",
    "hardened_clay_stained_black.png":      "black_terracotta.png",
    "hardened_clay.png":                    "terracotta.png",

    # Carpet (same colour pattern)
    "carpet_white.png":              "white_carpet.png",
    "carpet_orange.png":             "orange_carpet.png",
    "carpet_magenta.png":            "magenta_carpet.png",
    "carpet_light_blue.png":         "light_blue_carpet.png",
    "carpet_yellow.png":             "yellow_carpet.png",
    "carpet_lime.png":               "lime_carpet.png",
    "carpet_pink.png":               "pink_carpet.png",
    "carpet_gray.png":               "gray_carpet.png",
    "carpet_silver.png":             "light_gray_carpet.png",
    "carpet_cyan.png":               "cyan_carpet.png",
    "carpet_purple.png":             "purple_carpet.png",
    "carpet_blue.png":               "blue_carpet.png",
    "carpet_brown.png":              "brown_carpet.png",
    "carpet_green.png":              "green_carpet.png",
    "carpet_red.png":                "red_carpet.png",
    "carpet_black.png":              "black_carpet.png",

    # Rails
    "rail_normal.png":               "rail.png",
    "rail_normal_turned.png":        "rail_corner.png",
    "rail_golden.png":               "powered_rail.png",
    "rail_golden_powered.png":       "powered_rail_on.png",
    "rail_detector.png":             "detector_rail.png",
    "rail_detector_powered.png":     "detector_rail_on.png",
    "rail_activator.png":            "activator_rail.png",
    "rail_activator_powered.png":    "activator_rail_on.png",

    # Redstone
    "redstone_dust_cross.png":       "redstone_dust_dot.png",
    "redstone_dust_line.png":        "redstone_dust_line0.png",
    "redstone_lamp_off.png":         "redstone_lamp.png",
    "redstone_torch_on.png":         "redstone_torch.png",
    "torch_on.png":                  "torch.png",

    # Misc blocks
    "waterlily.png":                 "lily_pad.png",
    "portal.png":                    "nether_portal.png",
    "pumpkin_jack.png":              "jack_o_lantern.png",
    "nether_wart_stage_0.png":       "nether_wart_stage0.png",
    "nether_wart_stage_1.png":       "nether_wart_stage1.png",
    "nether_wart_stage_2.png":       "nether_wart_stage2.png",
    "cocoa_stage_0.png":             "cocoa_stage0.png",
    "cocoa_stage_1.png":             "cocoa_stage1.png",
    "cocoa_stage_2.png":             "cocoa_stage2.png",
    "carrots_stage_0.png":           "carrots_stage0.png",
    "carrots_stage_1.png":           "carrots_stage1.png",
    "carrots_stage_2.png":           "carrots_stage2.png",
    "carrots_stage_3.png":           "carrots_stage3.png",
    "potatoes_stage_0.png":          "potatoes_stage0.png",
    "potatoes_stage_1.png":          "potatoes_stage1.png",
    "potatoes_stage_2.png":          "potatoes_stage2.png",
    "potatoes_stage_3.png":          "potatoes_stage3.png",
    "double_plant_grass_bottom.png": "tall_grass_bottom.png",
    "double_plant_grass_top.png":    "tall_grass_top.png",
    "double_plant_fern_bottom.png":  "large_fern_bottom.png",
    "double_plant_fern_top.png":     "large_fern_top.png",
    "double_plant_sunflower_back.png":   "sunflower_back.png",
    "double_plant_sunflower_front.png":  "sunflower_front.png",
    "double_plant_sunflower_bottom.png": "sunflower_bottom.png",
    "double_plant_sunflower_top.png":    "sunflower_top.png",
    "double_plant_rose_bottom.png":      "rose_bush_bottom.png",
    "double_plant_rose_top.png":         "rose_bush_top.png",
    "double_plant_paeonia_bottom.png":   "peony_bottom.png",
    "double_plant_paeonia_top.png":      "peony_top.png",
    "double_plant_syringa_bottom.png":   "lilac_bottom.png",
    "double_plant_syringa_top.png":      "lilac_top.png",
    "mushroom_block_skin_stem.png":      "mushroom_stem.png",
    "mushroom_block_skin_red.png":       "red_mushroom_block.png",
    "mushroom_block_skin_brown.png":     "brown_mushroom_block.png",
    "quartz_block_chiseled.png":         "chiseled_quartz_block.png",
    "quartz_block_chiseled_top.png":     "chiseled_quartz_block_top.png",
    "quartz_block_lines.png":            "quartz_pillar.png",
    "quartz_block_lines_top.png":        "quartz_pillar_top.png",
    "grass_side_snowed.png":             "grass_block_snow.png",
    "mycelium_top.png":                  "mycelium_top.png",   # unchanged
    "mycelium_side.png":                 "mycelium_side.png",  # unchanged
}

# ---------------------------------------------------------------------------
# Item texture file renames (basenames only)
# Applied inside textures/item/ after folder rename.
# ---------------------------------------------------------------------------
ITEM_RENAMES = {
    # Food
    "seeds_wheat.png":               "wheat_seeds.png",
    "seeds_pumpkin.png":             "pumpkin_seeds.png",
    "seeds_melon.png":               "melon_seeds.png",
    "seeds_beetroot.png":            "beetroot_seeds.png",
    "fish_raw.png":                  "cod.png",
    "fish_cooked.png":               "cooked_cod.png",
    "fish_salmon_raw.png":           "salmon.png",
    "fish_salmon_cooked.png":        "cooked_salmon.png",
    "fish_clownfish_raw.png":        "tropical_fish.png",
    "fish_pufferfish_raw.png":       "pufferfish.png",
    "porkchop_raw.png":              "porkchop.png",
    "porkchop_cooked.png":           "cooked_porkchop.png",
    "beef_raw.png":                  "beef.png",
    "beef_cooked.png":               "cooked_beef.png",
    "chicken_raw.png":               "chicken.png",
    "chicken_cooked.png":            "cooked_chicken.png",
    "mutton_raw.png":                "mutton.png",
    "mutton_cooked.png":             "cooked_mutton.png",
    "rabbit_raw.png":                "rabbit.png",
    "rabbit_cooked.png":             "cooked_rabbit.png",

    # Doors
    "door_wood.png":                 "oak_door.png",
    "door_iron.png":                 "iron_door.png",
    "door_spruce.png":               "spruce_door.png",
    "door_birch.png":                "birch_door.png",
    "door_jungle.png":               "jungle_door.png",
    "door_acacia.png":               "acacia_door.png",
    "door_dark_oak.png":             "dark_oak_door.png",

    # Signs / boats
    "sign.png":                      "oak_sign.png",
    "boat.png":                      "oak_boat.png",

    # Minecarts
    "minecart_chest.png":            "chest_minecart.png",
    "minecart_furnace.png":          "furnace_minecart.png",
    "minecart_tnt.png":              "tnt_minecart.png",
    "minecart_hopper.png":           "hopper_minecart.png",

    # Dyes
    "dye_powder_black.png":          "ink_sac.png",
    "dye_powder_blue.png":           "lapis_lazuli.png",
    "dye_powder_brown.png":          "cocoa_beans.png",
    "dye_powder_cyan.png":           "cyan_dye.png",
    "dye_powder_gray.png":           "gray_dye.png",
    "dye_powder_green.png":          "cactus_green.png",
    "dye_powder_light_blue.png":     "light_blue_dye.png",
    "dye_powder_lime.png":           "lime_dye.png",
    "dye_powder_magenta.png":        "magenta_dye.png",
    "dye_powder_orange.png":         "orange_dye.png",
    "dye_powder_pink.png":           "pink_dye.png",
    "dye_powder_purple.png":         "purple_dye.png",
    "dye_powder_red.png":            "red_dye.png",
    "dye_powder_silver.png":         "light_gray_dye.png",
    "dye_powder_white.png":          "bone_meal.png",
    "dye_powder_yellow.png":         "dandelion_yellow.png",

    # Misc items
    "reeds.png":                     "sugar_cane.png",
    "comparator.png":                "comparator.png",        # unchanged
    "repeater.png":                  "repeater.png",          # unchanged
    "melon.png":                     "melon_slice.png",

    # Music discs
    "record_13.png":                 "music_disc_13.png",
    "record_cat.png":                "music_disc_cat.png",
    "record_blocks.png":             "music_disc_blocks.png",
    "record_chirp.png":              "music_disc_chirp.png",
    "record_far.png":                "music_disc_far.png",
    "record_mall.png":               "music_disc_mall.png",
    "record_mellohi.png":            "music_disc_mellohi.png",
    "record_stal.png":               "music_disc_stal.png",
    "record_strad.png":              "music_disc_strad.png",
    "record_ward.png":               "music_disc_ward.png",
    "record_11.png":                 "music_disc_11.png",
    "record_wait.png":               "music_disc_wait.png",
}

# ---------------------------------------------------------------------------
# Entity / mob texture renames
# Paths relative to assets/minecraft/textures/entity/
# old subpath → new subpath
# ---------------------------------------------------------------------------
MOB_RENAMES = {
    "zombie_pigman.png":             "piglin/zombified_piglin.png",
    "snowman.png":                   "snow_golem/snow_golem.png",
    "mooshroom/mooshroom.png":       "cow/mooshroom.png",
    "ocelot/ocelot.png":             "cat/ocelot.png",
    "ocelot/tuxedo.png":             "cat/black.png",
    "ocelot/red.png":                "cat/red.png",
    "ocelot/siamese.png":            "cat/siamese.png",
    "saddle.png":                    "pig/pig_saddle.png",
    "villager/priest.png":           "villager/cleric.png",
    "villager/smith.png":            "villager/armorer.png",
    "villager/blend.png":            "villager/weaponsmith.png",
    "horse/horse_armor_leather.png": "horse/leather_horse_armor.png",
    "horse/horse_armor_iron.png":    "horse/iron_horse_armor.png",
    "horse/horse_armor_gold.png":    "horse/golden_horse_armor.png",
    "horse/horse_armor_diamond.png": "horse/diamond_horse_armor.png",
    "guardian_elder.png":            "elder_guardian.png",
}

# ---------------------------------------------------------------------------
# Armor texture renames
# Paths relative to assets/minecraft/textures/
# Old location: models/armor/<file>
# New location: entity/equipment/humanoid/<file>  (layer 1 — helmet/chestplate/boots)
#               entity/equipment/humanoid_leggings/<file>  (layer 2 — leggings)
# ---------------------------------------------------------------------------
ARMOR_RENAMES = {
    # Chainmail
    "models/armor/chainmail_layer_1.png":        "entity/equipment/humanoid/chainmail.png",
    "models/armor/chainmail_layer_2.png":        "entity/equipment/humanoid_leggings/chainmail.png",
    # Diamond
    "models/armor/diamond_layer_1.png":          "entity/equipment/humanoid/diamond.png",
    "models/armor/diamond_layer_2.png":          "entity/equipment/humanoid_leggings/diamond.png",
    # Gold
    "models/armor/gold_layer_1.png":             "entity/equipment/humanoid/gold.png",
    "models/armor/gold_layer_2.png":             "entity/equipment/humanoid_leggings/gold.png",
    # Iron
    "models/armor/iron_layer_1.png":             "entity/equipment/humanoid/iron.png",
    "models/armor/iron_layer_2.png":             "entity/equipment/humanoid_leggings/iron.png",
    # Leather
    "models/armor/leather_layer_1.png":          "entity/equipment/humanoid/leather.png",
    "models/armor/leather_layer_2.png":          "entity/equipment/humanoid_leggings/leather.png",
    "models/armor/leather_layer_1_overlay.png":  "entity/equipment/humanoid/leather_overlay.png",
}

# ---------------------------------------------------------------------------
# Language file conversion
# .lang (key=value) → .json ({"key": "value"})
# ---------------------------------------------------------------------------
LANG_FORMAT = {
    "old_extension": ".lang",
    "new_extension": ".json",
    "folder":        "assets/minecraft/lang/",
}
