
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--Input", help = "Input directory of the images to be renamed")
args = parser.parse_args()

dir_path = args.Input



# Loop through all files in the directory
for filename in os.listdir(dir_path):
    # Check if file is a .png image
    if filename.endswith('.png'):
        # Get the file name without extension
        name = os.path.splitext(filename)[0]
        # Strip first 4 letters 
        new_name = name[4:] + '.png'
        # Construct full path to old and new names
        old_path = os.path.join(dir_path, filename)
        new_path = os.path.join(dir_path, new_name)
        # Rename the file
        os.rename(old_path, new_path)
