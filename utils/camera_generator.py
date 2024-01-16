from math import sin, cos, asin, acos, pi, radians
from scipy.spatial.transform import Rotation as R
from argparse import ArgumentParser
import numpy as np
import os
import pandas as pd
import yaml

def coordinates(fov_y):
    coordinate_list = list()
    # Retrieve camera poses for each of the image
    x = r * cos(2 * pi * i / args.number_of_views)
    z = r * sin(2 * pi * i / args.number_of_views)
    phi = 2 * pi * i / args.number_of_views + pi if i < args.number_of_views / 2 else 2 * pi * i / args.number_of_views - pi
    coords = (x, fov_y/2.0, z, 0, phi)
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
    q *= 0.5 / np.sqrt(t * R[2,2])
    return q

def retrieve_rotation_matrix(angle):
    yaw =radians(angle)
    roll = 0
    pitch = 0
    R_x = np.array([[cos(yaw), -sin(yaw), 0], [sin(yaw), cos(yaw), 0], [0, 0, 1]])
    R_y = np.array([[cos(roll), 0, sin(roll)], [0, 1, 0], [-sin(roll), 0, cos(roll)]])
    R_z = np.array([[1, 0 , 0], [0, cos(pitch), -sin(pitch)], [0, sin(pitch), cos(pitch)]])
    R = np.dot(R_x, R_y, R_z)
    return R

def calculate_translation_vector(R, C):
    translation_vector = np.dot(np.linalg.inv(-R.transpose()), C)
    return translation_vector

def metadata_to_intrinsics(d_source, d_patient, det_size):
    focal_length = 0
    principle_point = [0,0,0]
    return focal_length, principle_point

def write_yaml(yaml_data):
    with open('data.yml', 'w') as outfile:
        yaml.dump(yaml_data, outfile, default_flow_style=False)


if __name__ == "__main__":

    # Note to do: add required=True after finishing with tests
    parser = ArgumentParser("Coordinate Generator")
    parser.add_argument("--distance_source_to_patient", "-p", default=541, type=float)
    parser.add_argument("--distance_source_to_detector", "-d", default=949, type=float)
    parser.add_argument("--detector_size", "-s", default=350, type=float)
    parser.add_argument("--fov_x", "-x", default = 256, type=int)
    parser.add_argument("--fov_y", "-y", default = 175, type=int)
    parser.add_argument("--fov_z", "-z", default = 256, type=int)
    parser.add_argument("--number_of_views", "-v", default = 360, type=int)
    parser.add_argument("--height", "-he", default = 128, type=float)
    parser.add_argument("--width", "-w", default = 128, type=int)
    parser.add_argument("--output", "-o", default="cameras", type=str)

    args = parser.parse_args()

    assert args.distance_source_to_patient > 0, f"distance of source to patient must be greater than 0, got {args.distance_source_to_patient}"
    assert args.distance_source_to_detector > 0, f"distance of source to detector must be greater than 0, got {args.distance_source_to_detector}"
    assert args.detector_size > 0, f"detector size must be greater than 0, got {args.detector_size}"
    assert args.number_of_views > 0, f"views must be greater than 0, got {args.number_of_views}"
    assert args.width > 0, f"width must be greater than 0, got {args.width}"
    assert args.height > 0, f"height must be greater than 0, got {args.height}"

    os.makedirs(args.output, exist_ok=True)

    r = int(args.distance_source_to_detector/2)

    yaml_data = []

    for i in range(args.number_of_views):
        coords = coordinates(args.fov_y)
        # print(coords)
        entry_name = "image_" + str(i+1)
        Rot = retrieve_rotation_matrix(coords[0][4])
        tvec = calculate_translation_vector(Rot, coords[0][1:4])

        entry = {
            entry_name : [
                {
                    'intrinsics': {
                        'focal_length': args.distance_source_to_patient,
                        'principle_point': int(args.detector_size/2)
                    }, 
                    'extrinsics': {
                        'qvec': rotation_matrix_to_quaternion(Rot).tolist(),
                        #'qvec': Rot.tolist(),
                        'tvec': tvec.tolist()
                    },
                    'height': args.height,
                    'width': args.width
                }
            ]
        }
        yaml_data.append(entry)

        #import pdb; pdb.set_trace()

    write_yaml(yaml_data)
    