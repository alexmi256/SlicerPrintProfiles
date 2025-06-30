# What
This repo contains all machine, filament, and process configuration files found in Bambu Studio along side a combined version of the configs in cases where they inherit from other configs.

# Why
The current machines only support four nozzle sizes: 0.2mm, 0.4mm, 0.6mm, 0.8mm
If we want to use different nozzle sizes we will have to come up with our own profiles and these existing configs can help determine the settings for other files.
This repo also helps easily identify what the differences are between such configuration files.

# How
The Bambu Studio (and Orca Slider and probably other PrusaSlicer derivatives) store native configs at:
- “C:\Users\USERNAME\AppData\Roaming\BambuStudio\user\default\filament\base
Newly created configs are store at
- “C:\Users\USERNAME\AppData\Roaming\BambuStudio\user\default\filament\base

I've simply copied the whole `system` folder and removed any non-json files from it.

I've then run `create_combined_files.py` to produce files which check if an `inherits` key exists in the current config. 
If it does then it will load that parent config and apply the current config to the parent overwriting any values it had. This process is recursive.

Another thing it does is split up any values that come from a `_gcode` key. 
This is done so that we can more easily compare gcodde commands as they will now be listed line by line.
This does mean that we cannot directly use a `combined` file as a replacement

# Usage
## https://json-diff-viewer.lovable.app/
Use https://json-diff-viewer.lovable.app/ to compare the configurations that `create_combined_files.py` creates.
For now, I've excluded filaments from the comparables just because there are so many 

## create_combined_files.py
Run this script to generate all the `combined_*` files

# Notes and Weird Stuff
## General
- If a file does not have a nozzle size but other do, assume it's meant for a 0.4 nozzle (or 0.4 + 0.6)
- The X1 machine does not really exist anymore and AFAICT was the kickstarter version, X1C is the machine you should care about more
- The P1S uses configs from X1C

## Filament
These are the different filament/material profiles that are built in.

![material_settings.png](images/material_setting.png)

Not very useful besides seeing what differences a `Generic` and other brand filament have.

Covers settings under:
- Filament
- Cooling
- Settings Overrides
- Advanced
- Multimaterial
- Dependencies

Most changes done here will be regarding flow ratio, pressure advance, filament temps...

Example: `combined_generic_pla` vs `combined_bambu_pla_basic@bbl_x1c` (which should apply only to 0.4/6 nozzles are this config has separate files for 0.2)
```diff
diff --git a/system/BBL/filament/combined_generic_pla.json b/system/BBL/filament/combined_bambu_pla_basic_@bbl_x1c.json
index ee723fc..f5ba7c6 100644
--- a/system/BBL/filament/combined_generic_pla.json
+++ b/system/BBL/filament/combined_bambu_pla_basic_@bbl_x1c.json
@@ -16,17 +16,11 @@
     ],
     "compatible_printers": [
         "Bambu Lab X1 Carbon 0.4 nozzle",
-        "Bambu Lab X1 0.4 nozzle",
         "Bambu Lab X1 Carbon 0.6 nozzle",
-        "Bambu Lab X1 Carbon 0.8 nozzle",
-        "Bambu Lab X1 0.6 nozzle",
-        "Bambu Lab X1 0.8 nozzle",
         "Bambu Lab P1S 0.4 nozzle",
         "Bambu Lab P1S 0.6 nozzle",
-        "Bambu Lab P1S 0.8 nozzle",
         "Bambu Lab X1E 0.4 nozzle",
-        "Bambu Lab X1E 0.6 nozzle",
-        "Bambu Lab X1E 0.8 nozzle"
+        "Bambu Lab X1E 0.6 nozzle"
     ],
     "complete_print_exhaust_fan_speed": [
         "70"
@@ -52,7 +46,6 @@
     "counter_limit_min": [
         "-0.035"
     ],
-    "description": "The generic presets are conservatively tuned for compatibility with a wider range of filaments. For higher printing quality and speeds, please use Bambu filaments with Bambu presets.",
     "diameter_limit": [
         "50"
     ],
@@ -77,11 +70,14 @@
     "filament_adhesiveness_category": [
         "100"
     ],
+    "filament_change_length": [
+        "5"
+    ],
     "filament_cost": [
-        "20"
+        "24.99"
     ],
     "filament_density": [
-        "1.24"
+        "1.26"
     ],
     "filament_deretraction_speed": [
         "nil"
@@ -111,18 +107,18 @@
     "filament_flush_volumetric_speed": [
         "0"
     ],
-    "filament_id": "GFL99",
+    "filament_id": "GFA00",
     "filament_is_support": [
         "0"
     ],
     "filament_long_retractions_when_cut": [
-        "nil"
+        "1"
     ],
     "filament_long_retractions_when_ec": [
         "nil"
     ],
     "filament_max_volumetric_speed": [
-        "12"
+        "21"
     ],
     "filament_minimal_purge_on_wipe_tower": [
         "15"
@@ -131,7 +127,7 @@
         "0"
     ],
     "filament_prime_volume": [
-        "45"
+        "30"
     ],
     "filament_printable": [
         "3"
@@ -152,7 +148,7 @@
         "nil"
     ],
     "filament_retraction_distances_when_cut": [
-        "nil"
+        "18"
     ],
     "filament_retraction_distances_when_ec": [
         "nil"
@@ -167,7 +163,7 @@
         "nil"
     ],
     "filament_scarf_gap": [
-        "15%"
+        "0%"
     ],
     "filament_scarf_height": [
         "10%"
@@ -194,7 +190,7 @@
             "{elsif(bed_temperature[current_extruder] >50)||(bed_temperature_initial_layer[current_extruder] >50)}M106 P3 S150",
             "{elsif(bed_temperature[current_extruder] >45)||(bed_temperature_initial_layer[current_extruder] >45)}M106 P3 S50",
             "{endif}",
-            "",
+            "M142 P1 R35 S40",
             "{if activate_air_filtration[current_extruder] && support_air_filtration}",
             "M106 P3 S{during_print_exhaust_fan_speed_num[current_extruder]} ",
             "{endif}"
@@ -204,7 +200,7 @@
         "PLA"
     ],
     "filament_vendor": [
-        "Generic"
+        "Bambu Lab"
     ],
     "filament_wipe": [
         "nil"
@@ -244,14 +240,14 @@
         "55"
     ],
     "impact_strength_z": [
-        "10.0"
+        "13.8"
     ],
-    "inherits": "Generic PLA @base",
+    "inherits": "Bambu PLA Basic @base",
     "instantiation": "true",
     "long_retractions_when_ec": [
         "0"
     ],
-    "name": "Generic PLA",
+    "name": "Bambu PLA Basic @BBL X1C",
     "nozzle_temperature": [
         "220"
     ],
@@ -279,12 +275,12 @@
     "retraction_distances_when_ec": [
         "0"
     ],
-    "setting_id": "GFSL99",
+    "setting_id": "GFSA00",
     "slow_down_for_layer_cooling": [
         "1"
     ],
     "slow_down_layer_time": [
-        "8"
+        "4"
     ],
     "slow_down_min_speed": [
         "20"
```

- For some reason P1P is split off into its own folder
- For some reason 0.2 nozzles and 0.4/6/8 nozzle use different config, no idea why latter can be grouped up
- 0.8 nozzles sometimes have also different config files

## Machine
These are for machine setups i.e. what nozzle you have attached to the machine

![printer_settings.png](images/printer_settings.png)

Covers settings under:
- Basic Info
- Machine Gcode
- Multimaterial
- Extruder
- Motion Ability

The Extruder tab is where most changes will take place as well some gcode edits

## Process
These are for the different print/layer settings that will be used

![process.png](images/process.png)

# TODO
- [x] App for showing diffs between files
  - https://codesandbox.io/p/sandbox/jsdiffdiff2html-jrcxz?file=%2Fsrc%2FApp.js
  - https://observablehq.com/@sam-albers/diff-tool
  - https://github.com/kpdecker/jsdiff
  - https://github.com/rtfpessoa/diff2html
  - https://json-diff-viewer.lovable.app/
- [ ] A simple one page HTML file (no react BS) that can compare the combined configs in this repo
- [ ] Script for outputting a proper config file that deals with `inherits` and `_gcode` keys
- [ ] Remove `inherits` in combined files
- [ ] Get all the configs from Bambu Studio
- [x] Add extra info about the configs, i.e. names, weird stuff (0.2 treated differently that 0.4/6/8)
- [ ] Add info on modifications needed to get one of these profiles working
- [ ] Test out adding additional nozzle sizes to native Bambu Studio configs i.e. `BBL.json`
- [ ] Produce a tree of the different files
- [ ] Skip making combined diffs for files that are inbetween the tree 
