import os
from PIL import Image

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--Input", help = "Input directory of the images to be renamed")
args = parser.parse_args()

dir_path = args.Input

for filename in os.listdir(dir_path):
    if filename.endswith('.jpg') or filename.endswith('.png'): 
        image_path = os.path.join(dir_path, filename)
        image = Image.open(image_path).convert('RGB')
        image.save(image_path)
