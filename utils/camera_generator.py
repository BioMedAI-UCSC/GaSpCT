from math import sin, cos, asin, acos, pi
from argparse import ArgumentParser
import os
import pandas as pd
import yaml

def coordinates():
    parser = ArgumentParser("Coordinate Generator")
    parser.add_argument("--distance_source_to_patient", "-p", default=1, type=float)
    parser.add_argument("--distance_source_to_detector", "-d", default=1, type=float)
    parser.add_argument("--detector_size", "-s", default=1, type=float)
    parser.add_argument("--number_of_views", "-v", required=True, type=int)
    parser.add_argument("--output", "-o", default="cameras", type=str)

    args = parser.parse_args()

    assert args.distance_source_to_patient > 0, f"distance of source to patient must be greater than 0, got {args.distance_source_to_patient}"
    assert args.distance_source_to_detector > 0, f"distance of source to detector must be greater than 0, got {args.distance_source_to_detector}"
    assert args.detector_size > 0, f"detector size must be greater than 0, got {args.detector_size}"
    assert args.number_of_views > 0, f"views must be greater than 0, got {args.number_of_views}"

    os.makedirs(args.output, exist_ok=True)

    r = int(args.distance_source_to_detector/2)
    coordinate_list = list()

    # Retrieve camera poses for each of the image
    for i in range(args.views):
        x = r * cos(2 * pi * i / args.number_of_views)
        z = r * sin(2 * pi * i / args.number_of_views)
        phi = 2 * pi * i / args.number_of_views + pi if i < args.number_of_views / 2 else 2 * pi * i / args.number_of_views - pi

        coords = (x, 0, z, 0, phi)
        
        coordinate_list.append(coords)

    return coordinate_list

def pose_to_extrinsics(poses):
    translation_vector = [0, 0, 0]
    rotation_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    return translation_vector, rotation_matrix

def metadata_to_intrinsics(d_source, d_patient, det_size):
    focal_length = 0
    principle_point = [0,0,0]
    return focal_length, principle_point

def write_yaml(camera_extrinsics, camera_intrinsics):
    data = dict(
        Extrinsics = camera_extrinsics,
        Intrinsics = camera_intrinsics,
    )

    with open('data.yml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def main():
    coordinates()

main()