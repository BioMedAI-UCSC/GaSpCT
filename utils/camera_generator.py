from math import sin, cos, asin, acos, pi, radians, tan
from scipy.spatial.transform import Rotation as R
from argparse import ArgumentParser
import numpy as np
import os
import pandas as pd
import yaml
from graphics_utils import fov2focal

def coordinates(r, fov_y, number_of_views):
    coordinate_list = list()
    # Retrieve camera poses for each of the image
    x = r * cos(2 * pi * i / number_of_views)
    z = r * sin(2 * pi * i / number_of_views)
    phi = 2 * pi * i / number_of_views + pi if i < number_of_views / 2 else 2 * pi * i / number_of_views - pi
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
    output_file = 'camera_parameters.yml'
    with open(output_file, 'w') as f:
        for line in yaml_data:
            f.write(line)

def medical_to_true_fov(medical_fov, distance):
    return 2 * tan(medical_fov / (2 * distance))


if __name__ == "__main__":
    
    input_yaml_file = "ct_configuration.yml"
    with open(input_yaml_file) as f:
        ct_config = yaml.safe_load(f)

    assert int(ct_config['source_to_patient'] > 0), f"The distance from the source to patient (distance_source_to_patient) must be greater than 0, got {ct_config['source_to_patient']}"
    assert int(ct_config['source_to_detector'] > 0), f"The distance from the source to detector (distance_source_to_detector) must be greater than 0, got {ct_config['source_to_detector']}"
    assert int(ct_config['detector_size'] > 0), f"Detector size must be greater than 0, got {ct_config['detector_size']}"
    assert int(ct_config['scanner_fov_x'] > 0), f"fov_x must be greater than 0, got {ct_config['scanner_fox_x']}"
    assert int(ct_config['scanner_fov_y'] > 0), f"fov_y must be greater than 0, got {ct_config['scanner_fox_y']}"
    assert int(ct_config['scanner_fov_z'] > 0), f"fov_z must be greater than 0, got {ct_config['scanner_fox_z']}"
    assert int(ct_config['number_of_views'] > 0), f"Number of views must be greater than 0, got {ct_config['number_of_views']}"
    assert int(ct_config['height'] > 0), f"height must be greater than 0, got {ct_config['height']}"
    assert int(ct_config['width'] > 0), f"width must be greater than 0, got {ct_config['width']}"

    radius = int(ct_config['source_to_detector']/2)
    camera_poses = []

    for i in range(ct_config['number_of_views']):
        coords = coordinates(radius, int(ct_config['scanner_fov_y']), int(ct_config['number_of_views']))
        entry_name = "image_" + str(i+1)
        Rot = retrieve_rotation_matrix(coords[0][4])
        tvec = calculate_translation_vector(Rot, coords[0][1:4])

        entry = {
          entry_name: {
            'intrinsics': {
              'focal_length_x': fov2focal(medical_to_true_fov(int(ct_config['scanner_fov_x']), int(ct_config['source_to_patient'])), int(ct_config['detector_size'])),
              'focal_length_z': fov2focal(medical_to_true_fov(int(ct_config['scanner_fov_z']), int(ct_config['source_to_patient'])), int(ct_config['detector_size'])),
              'principle_point': int(ct_config['detector_size']/2)
            },
            'extrinsics': {
              'qvec': rotation_matrix_to_quaternion(Rot).tolist(),
              'tvec': tvec.tolist()
            },
            'height': int(ct_config['height']),
            'width': int(ct_config['width'])
          }
        }
        camera_poses.append(yaml.dump(entry, Dumper=yaml.Dumper))

        #import pdb; pdb.set_trace()

    write_yaml(camera_poses)
    