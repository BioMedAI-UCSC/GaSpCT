import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import math

def calculate_psnr(img1, img2, max_pixel=255.0):
    """
    Calculate Peak Signal-to-Noise Ratio between two images.
    
    Args:
        img1: First image array
        img2: Second image array
        max_pixel: Maximum possible pixel value (default: 255.0)
    
    Returns:
        PSNR value in decibels (dB)
    """
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(max_pixel / math.sqrt(mse))

def show_and_save_images_with_difference(image_path1, image_path2, output_dir="output5", figsize=(12, 6), max_diff=20):
    """
    Display and save two images side by side: the rendered image and the pixel-wise difference map.
    Uses a fixed scale for the difference visualization and calculates PSNR.
    
    Args:
        image_path1: Path to the ground truth image
        image_path2: Path to the rendered image
        output_dir: Directory to save output images
        figsize: Size of the figure (default: (12, 6))
        max_diff: Maximum value for the difference scale (default: 255 for 8-bit images)
    """
    # Set larger font size for all titles
    plt.rcParams['font.size'] = 14

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    def load_and_process_image(image_path):
        # Load and resize image to 128x128, convert to grayscale
        img = Image.open(image_path).convert('L')
        img = img.resize((128, 128), Image.Resampling.LANCZOS)
        return np.array(img)
    
    # Load both images
    img_array1 = load_and_process_image(image_path1)
    img_array2 = load_and_process_image(image_path2)
    
    # Calculate absolute difference between images
    difference = np.abs(img_array1.astype(float) - img_array2.astype(float))
    
    # Calculate and display PSNR
    psnr = calculate_psnr(img_array1, img_array2)
    print(f"\nPSNR between ground truth and rendered image: {psnr:.2f} dB")
    
    # Save individual images
    Image.fromarray(img_array2).save(os.path.join(output_dir, 'rendered.png'))
    Image.fromarray(difference.astype(np.uint8)).save(os.path.join(output_dir, 'difference.png'))
    
    # Create main figure with 1x2 grid
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Rendered image
    ax1.imshow(img_array2, cmap='gray', vmin=0, vmax=255)
    ax1.set_title('Rendered Image (128x128)', fontsize=16)
    ax1.axis('off')
    
    # Difference map with a colormap to highlight differences, using fixed scale
    im2 = ax2.imshow(difference, cmap='viridis', vmin=0, vmax=max_diff)
    ax2.set_title('Pixel-wise Difference', fontsize=16)
    ax2.axis('off')
    plt.colorbar(im2, ax=ax2, label='Absolute Difference')
    
    plt.tight_layout()
    
    # Save the complete comparison visualization
    fig.savefig(os.path.join(output_dir, 'comparison5.png'), 
                bbox_inches='tight', dpi=300)
    
    plt.show()

def main():
    """
    Example usage of the function.
    """
    # Replace with your image paths
    image_path1 = "0_xray0000.png"
    image_path2 = "rendered_5_00000.png"
    
    # Show images with difference visualization and save results
    show_and_save_images_with_difference(image_path1, image_path2)
    
if __name__ == "__main__":
    main()