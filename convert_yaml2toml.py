#!/usr/bin/env python
# -*- coding: utf-8 -*-
import toml
import yaml
import click
from collections import OrderedDict
from pathlib import Path

SCRIPT_DIR = str(Path(__file__).parent)

@click.command()
@click.option('--toml-path', '-t', default='{}/camera_parameter.toml'.format(SCRIPT_DIR))
@click.option('--toml-template-path', '-temp', default='{}/template.toml'.format(SCRIPT_DIR))
@click.option('--yaml-path', '-y', default='{}/camchain-.data.yaml'.format(SCRIPT_DIR))
def main(toml_path, toml_template_path, yaml_path):
    decoder = toml.TomlDecoder(_dict=OrderedDict)
    encoder = toml.TomlEncoder(_dict=OrderedDict)

    f_yaml = open(yaml_path, "r")
    data = yaml.load(f_yaml)

    toml.TomlEncoder = encoder
    dict_toml = toml.load(open(toml_template_path), _dict=OrderedDict, decoder=decoder)
    dict_toml["Rgb"]["fx"] = data["cam0"]["intrinsics"][0]
    dict_toml["Rgb"]["fy"] = data["cam0"]["intrinsics"][1]
    dict_toml["Rgb"]["cx"] = data["cam0"]["intrinsics"][2]
    dict_toml["Rgb"]["cy"] = data["cam0"]["intrinsics"][3]

    dict_toml["Rgb"]["k1"] = data["cam0"]["distortion_coeffs"][0]
    dict_toml["Rgb"]["k2"] = data["cam0"]["distortion_coeffs"][1]
    dict_toml["Rgb"]["k3"] = data["cam0"]["distortion_coeffs"][2]
    dict_toml["Rgb"]["k4"] = data["cam0"]["distortion_coeffs"][3]
    dict_toml["Rgb"]["k5"] = 0
    dict_toml["Rgb"]["k6"] = 0

    with open(toml_path, "w") as f:
        toml.encoder.dump(dict_toml, f)
        print("generated")


if __name__ == "__main__":
    main()