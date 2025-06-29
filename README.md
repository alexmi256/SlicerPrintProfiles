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


# Notes and Weird Stuff
## Filament
- For some reason P1P is split off into its own folder
- For some reason 0.2 nozzles and 0.4/6/8 nozzle use different config, no idea why latter can be grouped up 
## Machine
## Process

# TODO
- [ ] App for showing diffs between files
- [ ] Script for outputting a proper config file that deals with `inherits` and `_gcode` keys
- [ ] Remove `inherits` in combined files
- [ ] Get all the configs from Bambu Studio
- [ ] Add extra info about the configs, i.e. names, weird stuff (0.2 treated differently that 0.4/6/8)
- [ ] Add info on modifications needed to get one of these profiles working
- [ ] Test out adding additional nozzle sizes to native Bambu Studio configs i.e. `BBL.json`
