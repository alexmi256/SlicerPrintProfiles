import json
import logging
from json import JSONDecodeError
from pprint import pprint
from pathlib import Path
from copy import deepcopy

avaliable_json_files = { x.stem: x for x in  Path('system').glob("**/*.json")}
#pprint(avaliable_json_files)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def load_inherited_attributes(current_config, current_config_name='root'):
    if 'inherits' in current_config:
        logger.debug(f'Current config "{current_config_name}" has inherited attributes')
        inherits_name = current_config['inherits']

        if inherits_name in avaliable_json_files:
            logger.debug(f'Current config "{current_config_name}" inherits from "{inherits_name}"')
            with open(avaliable_json_files[inherits_name]) as f:
                inherited_config = json.load(f)
                inherited_config_resolved = load_inherited_attributes(deepcopy(inherited_config), inherits_name)
                inherited_config_resolved.update(current_config)
                return inherited_config_resolved
        else:
            logger.debug(f'In "{current_config_name}" "{inherits_name}" was mentioned but not found in config files')
    else:
        logger.debug(f'There was no inherits specified in the config files for config {current_config_name}')

    # By default we didn't do anything to current config
    return current_config


json_paths = {x.stem: x for x in Path('system/BBL').glob("**/*.json") if 'combined' not in x.stem}
files_for_diff_viewer = []

for json_path in json_paths.values():
    with open(json_path) as machine_json_file:
        logger.debug(f'Loading "{json_path}" as json')
        try:
            machine_json_content = json.load(machine_json_file)
            fully_loaded_config = load_inherited_attributes(machine_json_content, json_path.stem)
            # pprint(fully_loaded_config)

            for k, v in fully_loaded_config.items():
                if k.endswith('_gcode'):
                    if isinstance(v, str):
                        fully_loaded_config[k] = v.split('\n')
                    elif isinstance(v, list):
                        fully_loaded_config[k] = [i.split('\n') for i in v]
                    else:
                        logger.error(f'Config object had a "_gcode" key with a value that was neither a string or list of strings')

            if 'inherits' in fully_loaded_config:
                combined_file_name = 'combined_' + json_path.stem.lower().replace(' ', '_') + json_path.suffix
                combined_file_path = json_path.parent.joinpath(combined_file_name)
                logger.debug(f'Combined file path will be: {combined_file_path}')
                with open(combined_file_path, 'w') as combined_json_file:
                    logger.debug(f'Writing combined file to "{combined_file_path}"')
                    json.dump(fully_loaded_config, combined_json_file, indent=4, sort_keys=True)
                    logger.debug(f'Writing combined file to "{combined_file_path}" success')
                    value_name = f'https://raw.githubusercontent.com/alexmi256/SlicerPrintProfiles/refs/heads/main/{combined_file_path}'
                    label_name = combined_file_name
                    if 'filament' not in str(combined_file_path):
                        files_for_diff_viewer.append(f"{{ value: '{value_name}', label: '{label_name}' }},")
            else:
                logger.debug(f'Skipping output for parent machine: {json_path.stem}')
        except JSONDecodeError as e:
            logger.error(f'Could not load "{json_path}" as json: {e}')
            continue

for js_code_for_diff_viewer in sorted(files_for_diff_viewer):
    print(js_code_for_diff_viewer)
