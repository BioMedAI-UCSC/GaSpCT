from math import sin, cos, asin, acos, pi
from argparse import ArgumentParser
import os
import pandas as pd

def coordinates():
    parser = ArgumentParser("Coordinate Generator")
    parser.add_argument("--camera_extrinsic", default=1, type=float)
    parser.add_argument("--camera_intrinsic", default=1, type=float)
    parser.add_argument("--views", "-v", required=True, type=int)
    parser.add_argument("--output", "-o", default="cameras", type=str)

    args = parser.parse_args()

    assert args.camera_extrinsic > 0, f"camera_extrinsic must be greater than 0, got {args.camera_extrinsic}"
    assert args.camera_intrinsic > 0, f"camera_intrinsic must be greater than 0, got {args.camera_intrinsic}"
    assert args.views > 0, f"views must be greater than 0, got {args.views}"

    os.makedirs(args.output, exist_ok=True)

    r = args.camera_extrinsic
    coordinate_list = list()

    for i in range(args.views):
        x = r * cos(2 * pi * i / args.views)
        z = r * sin(2 * pi * i / args.views)
        phi = 2 * pi * i / args.views + pi if i < args.views / 2 else 2 * pi * i / args.views - pi

        coords = (x, 0, z, 0, phi)
        
        coordinate_list.append(coords)

    file_text = f"Extrinsic: {r}\nIntrinsic: {args.camera_intrinsic}\n"

    with open(args.output + "/cameras.txt", "w") as file:
        file.write(file_text + str(coordinate_list))

def coords_to_quaternion(coordinates, intrinsic, point_cloud):
    points_in_view = []

    

    return points_in_view

def main():
    coordinates()

main()