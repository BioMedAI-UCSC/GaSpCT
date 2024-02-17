import os
import argparse
import imageio.v2 as imageio


def create_gif(input_dir, output_dir):
    # Dictionary to store images for each prefix
    prefix_images = {}

    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".png"):
            image_path = os.path.join(input_dir, filename)
            prefix = filename.split('_')[0]

            # Get or create list of images for the prefix
            if prefix not in prefix_images:
                prefix_images[prefix] = []

            # Load and append the image to the list
            image = imageio.imread(image_path)
            prefix_images[prefix].append(image)

    # Save images for each prefix as GIF files
    for prefix, images in prefix_images.items():
        gif_name = prefix + "_gif.gif"
        output_file = os.path.join(output_dir, gif_name)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        imageio.mimsave(output_file, images)
        print(f'saving {output_file}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a GIF from images in a directory.")
    parser.add_argument("--input_directory", help="Input directory containing images (e.g., './input_images')")
    parser.add_argument("--output_directory", help="Output GIF file name (e.g., 'output.gif')")

    args = parser.parse_args()

    create_gif(args.input_directory, args.output_directory)
