import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
import os

def show_and_save_two_images_with_zoomed_patches(image_path1, image_path2, output_dir="output", patch_size=32, figsize=(12, 12)):
    """
    Display and save two grayscale images with their zoomed-in views of selected patches.
    Also saves separate images showing the bounding boxes.
    
    Args:
        image_path1: Path to the first input image
        image_path2: Path to the second input image
        output_dir: Directory to save output images
        patch_size: Size of the square patch to zoom (default: 32)
        figsize: Size of the figure (default: (12, 12))
    """
    # Set larger font size for all titles
    plt.rcParams['font.size'] = 14

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    def process_single_image(image_path, index):
        # Load and resize image to 128x128, convert to grayscale
        img = Image.open(image_path).convert('L')
        img = img.resize((128, 128), Image.Resampling.LANCZOS)
        img_array = np.array(img)
        
        # Calculate patch coordinates (center of the image)
        start_row = (128 - patch_size) // 2 + 18
        start_col = (128 - patch_size) // 2 + 18
        
        # Extract the patch
        patch = img_array[start_row:start_row+patch_size, 
                         start_col:start_col+patch_size]
        
        # Save full image and patch
        Image.fromarray(img_array).save(
            os.path.join(output_dir, f'full_image_{index}.png'))
        Image.fromarray(patch).save(
            os.path.join(output_dir, f'zoomed_patch_{index}.png'))
        
        # Create and save image with bounding box
        fig_box, ax_box = plt.subplots(figsize=(6, 6))
        ax_box.imshow(img_array, cmap='gray')
        ax_box.add_patch(Rectangle((start_col, start_row), 
                                 patch_size, patch_size,
                                 fill=False, color='red', linewidth=2))
        ax_box.axis('off')
        fig_box.tight_layout(pad=0)
        fig_box.savefig(os.path.join(output_dir, f'image_with_box_{index}.png'), 
                       bbox_inches='tight', dpi=300, pad_inches=0)
        plt.close(fig_box)
        
        return img_array, patch, start_row, start_col
    
    # Process both images
    img_array1, patch1, start_row1, start_col1 = process_single_image(image_path1, 1)
    img_array2, patch2, start_row2, start_col2 = process_single_image(image_path2, 2)
    
    # Create main figure with 2x2 grid
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
    
    # First image and its patch
    ax1.imshow(img_array1, cmap='gray')
    ax1.add_patch(Rectangle((start_col1, start_row1), 
                          patch_size, patch_size,
                          fill=False, color='red', linewidth=2))
    ax1.set_title('Ground Truth Image (128x128)', fontsize=16)
    ax1.axis('off')
    
    ax2.imshow(patch1, cmap='gray', interpolation='nearest')
    ax2.set_title(f'Ground Truth Image Patch ({patch_size}x{patch_size})', fontsize=16)
    ax2.axis('off')
    
    # Second image and its patch
    ax3.imshow(img_array2, cmap='gray')
    ax3.add_patch(Rectangle((start_col2, start_row2), 
                          patch_size, patch_size,
                          fill=False, color='red', linewidth=2))
    ax3.set_title('Rendered Image (128x128)', fontsize=16)
    ax3.axis('off')
    
    ax4.imshow(patch2, cmap='gray', interpolation='nearest')
    ax4.set_title(f'Rendered Image Patch ({patch_size}x{patch_size})', fontsize=16)
    ax4.axis('off')
    
    plt.tight_layout()
    
    # Save the complete comparison visualization
    fig.savefig(os.path.join(output_dir, 'comparison.png'), 
                bbox_inches='tight', dpi=300)
    
    plt.show()

def main():
    """
    Example usage of the function.
    """
    # Replace with your image paths
    image_path1 = "image1.png"
    image_path2 = "image2.png"
    
    # Show images with zoomed patches and save results
    show_and_save_two_images_with_zoomed_patches(image_path1, image_path2)
    
if __name__ == "__main__":
    main()