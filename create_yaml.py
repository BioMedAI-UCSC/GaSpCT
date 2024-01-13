import argparse
import copy
import os
import yaml

def parse_args():
    parser = argparse.ArgumentParser(
        description="Intrinsic & Extrinsic Camera Params YAML creator"
    )
    parser.add_argument(
        "--model", "-m", type=str, required=True,
        help="Path to the COLMAP cameras and images text files directory"
    )
    parser.add_argument(
        "--output", "-o", type=str, default="cam_config.yaml"
    )
    parser.add_argument(
        "--images_txt", "-i", type=str, default="images.txt",
        help="Name of the camera extrinsic parameters file"
    )
    parser.add_argument(
        "--cameras_txt", "-c", type=str, default="cameras.txt",
        help="Name of the cameras intrinsic parameters file"
    )
    args = parser.parse_args()
    args.images_txt = os.path.join(args.model, args.images_txt)
    args.cameras_txt = os.path.join(args.model, args.cameras_txt)
    args.output = os.path.join(args.model, args.output)

    if not os.path.exists(args.images_txt):
        raise FileNotFoundError(f"Missing {args.images_txt}")

    if not os.path.exists(args.cameras_txt):
        raise FileNotFoundError(f"Missing {args.cameras_txt}")
    
    return args

def read_extrinsics_text(path, intrinsic):
    """
    Taken from https://github.com/colmap/colmap/blob/dev/scripts/python/read_write_model.py
    """
    images = {}
    with open(path, "r") as fid:
        while True:
            line = fid.readline()
            if not line:
                break
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                temp = {}
                elems = line.split()
                temp["extrinsics"] = {
                    "qvec" : list(map(float, elems[1:5])),
                    "tvec" : list(map(float, elems[5:8]))
                }
                cam_id = int(elems[8])
                image_name = elems[9]
                images[image_name] = {}
                images[image_name].update(temp)
                images[image_name].update(copy.deepcopy(intrinsic[cam_id]))
                elems = fid.readline().split()
    return images

def read_intrinsics_text(path):
    """
    Taken from https://github.com/colmap/colmap/blob/dev/scripts/python/read_write_model.py
    """
    cameras = {}
    with open(path, "r") as fid:
        while True:
            line = fid.readline()
            if not line:
                break
            line = line.strip()
            if len(line) > 0 and line[0] != "#":
                elems = line.split()
                camera_id = int(elems[0])
                model = elems[1]
                assert model == "PINHOLE", "While the loader support other types, the rest of the code assumes PINHOLE"
                width = int(elems[2])
                height = int(elems[3])
                params = list(map(float, elems[4:]))
                cameras[camera_id] = {
                    "width" : width,
                    "height" : height,
                    "intrinsics" : {
                      "focal_length_x" : params[0],
                      "focal_length_z" : params[1]  
                    }
                }
    return cameras

def main(args):
    intrinsic = read_intrinsics_text(args.cameras_txt)
    config = read_extrinsics_text(args.images_txt, intrinsic)

    with open(args.output, 'w') as writer:
        yaml.dump(config, writer, default_flow_style=False)

if __name__=="__main__":
    main(parse_args())