#!/usr/bin/env python
# -*- coding: utf-8 -*-
import toml
import yaml
import sys
import glob
import click
import time
from collections import OrderedDict
from pathlib import Path


SCRIPT_DIR = str(Path(__file__).parent)


def get_see3cam_device_id():
    count = 0
    while True:
        see3cam_path = glob.glob("/dev/v4l/by-id/usb-e-con*")
        if len(see3cam_path) == 0:
            sys.stdout.write("\rWaiting for device detection (see3cam)" + "." * count)
            time.sleep(1)
            sys.stdout.flush()
            count += 1
        else:
            break
    see3cam_path_list = glob.glob("/dev/v4l/by-id/usb-e-con*-video-index0")
    return see3cam_path_list[0]


@click.command()
@click.option('--toml-path', '-t', default='{}/camera_parameter.toml'.format(SCRIPT_DIR))
@click.option('--toml-template-path', '-temp', default='{}/template.toml'.format(SCRIPT_DIR))
@click.option('--yaml-path', '-y', default='{}/camchain-.data.yaml'.format(SCRIPT_DIR))
@click.option('--fill-see3cam-id', '-s3c', is_flag=True)
def main(toml_path, toml_template_path, yaml_path, fill_see3cam_id):
    decoder = toml.TomlDecoder(_dict=OrderedDict)
    encoder = toml.TomlEncoder(_dict=OrderedDict)

    f_yaml = open(yaml_path, "r")
    data = yaml.load(f_yaml)

    toml.TomlEncoder = encoder
    dict_toml = toml.load(open(toml_template_path), _dict=OrderedDict, decoder=decoder)
    if fill_see3cam_id:
        dict_toml["Rgb"]["device_id"] = get_see3cam_device_id()

    dict_toml["Rgb"]["width"] = data["cam0"]["resolution"][0]
    dict_toml["Rgb"]["height"] = data["cam0"]["resolution"][1]

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