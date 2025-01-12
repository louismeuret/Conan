import yaml

software_config = {
    "input": {
        "receptor": "",
        "flex": "",
        "ligand": ""
    },
    "search_space": {
        "center_x": 0.0,
        "center_y": 0.0,
        "center_z": 0.0,
        "size_x": 0.0,
        "size_y": 0.0,
        "size_z": 0.0
    },
    "output": {
        "out": "",
        "log": ""
    },
    "misc": {
        "cpu": 1,
        "seed": None,
        "exhaustiveness": 8,
        "num_modes": 9,
        "energy_range": 3
    },
    "config": "",
    "info": {
        "help": False,
        "help_advanced": False,
        "version": False
    }
}

with open('vina.yaml', 'w') as file:
    yaml.dump(software_config, file, default_flow_style=False)

