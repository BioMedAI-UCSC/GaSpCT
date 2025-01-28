import numpy as np
from skimage.transform import radon, iradon
import matplotlib.pyplot as plt
from skimage.data import shepp_logan_phantom

# Create the Shepp-Logan phantom
phantom = shepp_logan_phantom()

# Set up angles for normal and sparse view sampling
theta_normal = np.linspace(0., 180., 180)  # 180 projections (1 degree steps)
theta_sparse = np.linspace(0., 180., 36)   # 36 projections (5 degree steps)

# Generate sinograms
sinogram_normal = radon(phantom, theta=theta_normal)
sinogram_sparse = radon(phantom, theta=theta_sparse)

# Reconstruct images
reconstruction_normal = iradon(sinogram_normal, theta=theta_normal, filter_name='ramp')
reconstruction_sparse = iradon(sinogram_sparse, theta=theta_sparse, filter_name='ramp')

# Set up the figure with larger size and more vertical space
plt.figure(figsize=(15, 11))  # Increased height from 10 to 11

# Plot original phantom
plt.subplot(231)
plt.imshow(phantom, cmap='gray')
plt.title('Original Phantom', fontsize=14, pad=20)  # Added padding
plt.axis('off')

# Plot normal-view sinogram
plt.subplot(232)
plt.imshow(sinogram_normal, cmap='gray', aspect='auto')
plt.title('Normal-view Sinogram\n(180 projections)', fontsize=14, pad=20)  # Added padding
plt.axis('off')

# Plot normal-view reconstruction
plt.subplot(233)
plt.imshow(reconstruction_normal, cmap='gray')
plt.title('Normal-view Reconstruction', fontsize=14, pad=20)  # Added padding
plt.axis('off')

# Plot phantom again for comparison
plt.subplot(234)
plt.imshow(phantom, cmap='gray')
plt.title('Original Phantom', fontsize=14)
plt.axis('off')

# Plot sparse-view sinogram
plt.subplot(235)
plt.imshow(sinogram_sparse, cmap='gray', aspect='auto')
plt.title('Sparse-view Sinogram\n(36 projections)', fontsize=14)
plt.axis('off')

# Plot sparse-view reconstruction
plt.subplot(236)
plt.imshow(reconstruction_sparse, cmap='gray')
plt.title('Sparse-view Reconstruction', fontsize=14)
plt.axis('off')

# Add a main title with more space
plt.suptitle('Comparison of Normal vs Sparse-view CBCT Reconstruction', 
             fontsize=16, 
             y=0.98)  # Moved title up

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjusted rect parameter to leave more space for title

# Save the figure with high DPI for better quality
plt.savefig('ct_reconstruction_comparison.png', dpi=300, bbox_inches='tight')

# Display the figure
plt.show()

# Calculate and print the mean squared error between reconstructions and original phantom
mse_normal = np.mean((phantom - reconstruction_normal) ** 2)
mse_sparse = np.mean((phantom - reconstruction_sparse) ** 2)
print(f"Mean Squared Error (Normal-view): {mse_normal:.6f}")
print(f"Mean Squared Error (Sparse-view): {mse_sparse:.6f}")