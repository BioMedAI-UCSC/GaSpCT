from math import sin, cos, asin, acos, pi
from scipy.spatial.transform import Rotation as R
from argparse import ArgumentParser
import numpy as np
import os
import pandas as pd
import yaml

def coordinates():
    coordinate_list = list()
    # Retrieve camera poses for each of the image
    x = r * cos(2 * pi * i / args.number_of_views)
    z = r * sin(2 * pi * i / args.number_of_views)
    phi = 2 * pi * i / args.number_of_views + pi if i < args.number_of_views / 2 else 2 * pi * i / args.number_of_views - pi
    coords = (x, 0, z, 0, phi)
    coordinate_list.append(coords)
    return coordinate_list

def rotation_matrix_to_quaternion(R):
    q = np.empty((4, ))
    t = np.trace(R)
    if t > 0:
        q[0] = t + 1
        q[1] = R[1,2] - R[2,1]
        q[2] = R[2,0] - R[0,2] 
        q[3] = R[0,1] - R[1,0]
    else:
        i, j, k = 0, 1, 2
        if R[1,1] > R[0,0]:
            i, j, k = 1, 2, 0
        if R[2,2] > R[i,i]:
            i, j, k = 2, 0, 1
        t = R[i,i] - (R[j,j] + R[k,k]) + 1
        q[i] = t
        q[j] = R[i,j] + R[j,i]
        q[k] = R[k,i] + R[i,k]
        q[3] = R[k,j] - R[j,k] 
    q *= 0.5 / np.sqrt(t * R[3,3])
    return q

def retrieve_rotation_matrices(angle):
    yaw = radians(angle)
    roll = 0
    pitch = 0
    R_x = [[cos(yaw), -sin(yaw), 0], [sin(yaw), cos(yaw), 0], [0, 0, 1]]]
    R_y = [[cos(roll), 0, sin(roll)], [0, 1, 0], [-sin(roll), 0, cos(roll)]]
    R_z = [[1, 0 , 0], [0, cos(pitch), -sin(pitch)], [0, sin(pitch), cos(pitch)]]
    R = np.dot(R_x, R_y, R_z)
    return R

def pose_to_extrinsics(poses):
    translation_vector = [0, 0, 0]
    rotation_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    return translation_vector, rotation_matrix

def metadata_to_intrinsics(d_source, d_patient, det_size):
    focal_length = 0
    principle_point = [0,0,0]
    return focal_length, principle_point

def write_yaml(yaml_data):
    with open('data.yml', 'w') as outfile:
        yaml.dump(yaml_data, outfile, default_flow_style=False)


if __name__ == "__main__":

    parser = ArgumentParser("Coordinate Generator")
    parser.add_argument("--distance_source_to_patient", "-p", default=541, type=float)
    parser.add_argument("--distance_source_to_detector", "-d", default=949, type=float)
    parser.add_argument("--detector_size", "-s", default=350, type=float)
    parser.add_argument("--number_of_views", "-v", default = 360, required=True, type=int)
    parser.add_argument("--height", "-h", default = 128, type=float)
    parser.add_argument("--width", "-w", default = 128, type=int)
    parser.add_argument("--output", "-o", default="cameras", type=str)

    args = parser.parse_args()

    assert args.distance_source_to_patient > 0, f"distance of source to patient must be greater than 0, got {args.distance_source_to_patient}"
    assert args.distance_source_to_detector > 0, f"distance of source to detector must be greater than 0, got {args.distance_source_to_detector}"
    assert args.detector_size > 0, f"detector size must be greater than 0, got {args.detector_size}"
    assert args.number_of_views > 0, f"views must be greater than 0, got {args.number_of_views}"
    assert args.detector_size > 0, f"detector size must be greater than 0, got {args.detector_size}"
    assert args.number_of_views > 0, f"views must be greater than 0, got {args.number_of_views}"

    os.makedirs(args.output, exist_ok=True)

    r = int(args.distance_source_to_detector/2)

    yaml_data = {}

    for i in range(args.number_of_views):
        coords = coordinates()
        entry_name = "image_" + str(i+1)
        Rot = retrieve_rotation_matrices(coords[4])
        yaml_data[entry_name]['intrinsics']['focal_length'] = args.distance_source_to_patient
        yaml_data[entry_name]['intrinsics']['principle_point'] = []
        yaml_data[entry_name]['extrinsics']['qvec'] = R.as_quat(Rot)
        yaml_data[entry_name]['extrinsics']['tvec'] = []
        yaml_data[entry_name]['height'] = args.height
        yaml_data[entry_name]['width'] = args.width
    write_yaml(yaml_data)