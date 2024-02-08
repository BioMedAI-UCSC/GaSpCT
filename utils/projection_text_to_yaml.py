from math import sin, cos, asin, acos, pi, radians, tan
from scipy.spatial.transform import Rotation as R
from argparse import ArgumentParser
import numpy as np
import os
import pandas as pd
import yaml
import argparse
from graphics_utils import fov2focal

def rotation_matrix_to_quaternion(rotation_matrix):
    trace = np.trace(rotation_matrix)

    if trace > 0:
        S = np.sqrt(trace + 1.0) * 2.0
        qw = 0.25 * S
        qx = (rotation_matrix[2, 1] - rotation_matrix[1, 2]) / S
        qy = (rotation_matrix[0, 2] - rotation_matrix[2, 0]) / S
        qz = (rotation_matrix[1, 0] - rotation_matrix[0, 1]) / S
    elif (rotation_matrix[0, 0] > rotation_matrix[1, 1]) and (rotation_matrix[0, 0] > rotation_matrix[2, 2]):
        S = np.sqrt(1.0 + rotation_matrix[0, 0] - rotation_matrix[1, 1] - rotation_matrix[2, 2]) * 2.0
        qw = (rotation_matrix[2, 1] - rotation_matrix[1, 2]) / S
        qx = 0.25 * S
        qy = (rotation_matrix[0, 1] + rotation_matrix[1, 0]) / S
        qz = (rotation_matrix[0, 2] + rotation_matrix[2, 0]) / S
    elif rotation_matrix[1, 1] > rotation_matrix[2, 2]:
        S = np.sqrt(1.0 + rotation_matrix[1, 1] - rotation_matrix[0, 0] - rotation_matrix[2, 2]) * 2.0
        qw = (rotation_matrix[0, 2] - rotation_matrix[2, 0]) / S
        qx = (rotation_matrix[0, 1] + rotation_matrix[1, 0]) / S
        qy = 0.25 * S
        qz = (rotation_matrix[1, 2] + rotation_matrix[2, 1]) / S
    else:
        S = np.sqrt(1.0 + rotation_matrix[2, 2] - rotation_matrix[0, 0] - rotation_matrix[1, 1]) * 2.0
        qw = (rotation_matrix[1, 0] - rotation_matrix[0, 1]) / S
        qx = (rotation_matrix[0, 2] + rotation_matrix[2, 0]) / S
        qy = (rotation_matrix[1, 2] + rotation_matrix[2, 1]) / S
        qz = 0.25 * S

    return np.array([qw, qx, qy, qz])

def write_yaml(yaml_data, output_file):
    with open(output_file, 'w') as f:
        for line in yaml_data:
            f.write(line)

def parse_text_file(file_path):
    extrinsic_found = False
    intrinsic_found = False
    extrinsic_data = []
    intrinsic_data = []

    with open(file_path, 'r') as file:
        for line in file:
            if "extrinsic" in line.lower():
                extrinsic_found = True
                continue
            elif "intrinsic" in line.lower():
                extrinsic_found = False
                intrinsic_found = True
                continue

            if extrinsic_found:
                # Save top right 3 rows before "intrinsic"
                extrinsic_data.append(line.strip().split())

            if intrinsic_found:
                # Save diagonal below "intrinsic"
                intrinsic_data.append(float(line.strip().split()[len(intrinsic_data)]))

    # Convert lists to NumPy arrays
    extrinsic_data = np.array(extrinsic_data, dtype=float)[:-1]
    intrinsic_data = np.array(intrinsic_data, dtype=float)

    return extrinsic_data, intrinsic_data

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = "Input directory of text files with projection data")
    parser.add_argument("-o", "--Output", help = "Output file naming")
    args = parser.parse_args()

    directory_path = args.Input
    output_file = args.Output

    text_files = [file for file in os.listdir(directory_path) if file.endswith('.txt')]

    camera_poses = []

    for text_file in text_files:
        file_path = os.path.join(directory_path, text_file)

        extrinsic_data, intrinsic_data = parse_text_file(file_path)
        entry_name = (text_file[-8:])[:4] + ".png"
        
        # Specify before running
        image_dimension = [128, 128]

        Rot = np.delete(extrinsic_data, 3, axis=1)
        tvec = extrinsic_data[:, 3]

        entry = {
          entry_name: {
              'intrinsics': {
                'focal_length_x': float(intrinsic_data[0]/intrinsic_data[2]),
                'focal_length_z': float(intrinsic_data[1]/intrinsic_data[2]),
                'principle_point': 0
              },
              'extrinsics': {
                  'qvec': rotation_matrix_to_quaternion(Rot).tolist(),
                  'tvec': tvec.tolist()
                },
                'height': int(image_dimension[0]),
                'width': int(image_dimension[1])
          }
        }
        camera_poses.append(yaml.dump(entry, Dumper=yaml.Dumper))

    write_yaml(camera_poses, output_file)