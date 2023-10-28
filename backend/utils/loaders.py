
from typing import *
import os
import json
from yaml import safe_load

def yml_loader(yml_path: Union[str, os.PathLike]):
    with open(yml_path, "r") as ymf:
        config = safe_load(ymf)
    
    return config

def load_to_json(configs: Dict[str, Any], run_name: str):
    json_file_path = f"training_config_{run_name}.json"
    with open(json_file_path, "w+") as fle:
        json.dump(configs, fle)
    
    return json_file_path