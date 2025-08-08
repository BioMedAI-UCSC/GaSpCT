import numpy as np
import torch
import torch.nn as nn
from plyfile import PlyData, PlyElement
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scene import GaussianModel
from scene import Scene
from utils.general_utils import build_rotation, build_scaling_rotation
import argparse
from tqdm import tqdm 
from PIL import Image

def load_ply_file(gaussian_model: GaussianModel, ply_path:str) -> None:
    if not os.path.exists(ply_path):
        raise FileNotFoundError(f"PLY file not found: {ply_path}")

    print(f"Loading PLY file: {ply_path}")
    gaussian_model.load_ply(ply_path)
    print(f"Loaded {gaussian_model._xyz.shape[0]} Gaussian points")
    
def slice_gaussian(
        ply_path: str,
        sh_degree: int,
        axis:str = 'y',
        coordinate:float = 0.0,
        resolution:tuple = (128, 128),
        k_nearest:int = 20,
        save_path:str = "."
    ) -> None:
    gaussian_model = GaussianModel(sh_degree)
    
    load_ply_file(gaussian_model, ply_path)
    
    if axis == 'z':
        u_axis, v_axis, fixed_axis = 0, 1, 2  # X, Y axes for the plane
        axis_names = ('X', 'Y')
    elif axis == 'y':
        u_axis, v_axis, fixed_axis = 0, 2, 1  # X, Z axes for the plane
        axis_names = ('X', 'Z')
    elif axis == 'x':
        u_axis, v_axis, fixed_axis = 1, 2, 0  # Y, Z axes for the plane
        axis_names = ('Y', 'Z')
    else:
        raise ValueError(f"Invalid axis: {axis}. Must be 'x', 'y', or 'z'")
    
    xyz = gaussian_model._xyz.detach().cpu().numpy()
    min_bounds = np.min(xyz, axis=0)
    max_bounds = np.max(xyz, axis=0)
    u_min, u_max = min_bounds[u_axis], max_bounds[u_axis]
    v_min, v_max = min_bounds[v_axis], max_bounds[v_axis]
    
    pixel_width = (u_max - u_min) / resolution[0]
    pixel_height = (v_max - v_min) / resolution[1]
    
    # pixel grid:
    u_coords = torch.linspace(u_min + pixel_width/2, u_max - pixel_width/2, resolution[0], device='cuda')
    v_coords = torch.linspace(v_min + pixel_height/2, v_max - pixel_height/2, resolution[1], device='cuda')
    
    print(f"Computing single layer slice with {k_nearest} nearest Gaussians per pixel")
    print(f"Slice at {axis}={coordinate}, resolution: {resolution[0]}×{resolution[1]}")
    print(f"Pixel size: {pixel_width:.6f} x {pixel_height:.6f} world units")

    xyz = gaussian_model._xyz
    
    colors = torch.zeros(resolution[1], resolution[0], 3, device='cuda', dtype=torch.float32)
    
    opacities = gaussian_model.get_opacity.squeeze(-1) # [N]
    scalings = gaussian_model.get_scaling  # [N, 3]
    rotations = gaussian_model._rotation  # [N, 4]
    
    L = build_scaling_rotation(scalings, rotations)  # [N, 3, 3]
    covariances = L @ L.transpose(-1, -2)  # [N, 3, 3]
    
    if hasattr(gaussian_model, '_features_dc'):
        gaussian_colors = gaussian_model._features_dc[:, :, 0]  # [N, 3]
        gaussian_colors = torch.sigmoid(gaussian_colors)
    else:
        gaussian_colors = torch.ones(len(xyz), 3, device='cuda')
        
    total_pixels = resolution[0] * resolution[1]
    
    with tqdm(total=total_pixels, unit="pixel", desc="Processing pixels") as pbar:
        processed_pixels = 0
        
        for i, v in enumerate(v_coords):
            for j, u in enumerate(u_coords):
                pixel_point = torch.zeros(3, device='cuda')
                pixel_point[u_axis] = u
                pixel_point[v_axis] = v
                pixel_point[fixed_axis] = coordinate
                
                diffs = xyz - pixel_point.unsqueeze(0)  # [N, 3]
                distances = torch.norm(diffs, dim=1)  # [N]
                    
                _, nearest_indices = torch.topk(distances, min(k_nearest, len(distances)), largest=False)
                
                total_value = 0.0
                weighted_color = torch.zeros(3, device='cuda')
                total_weight = 0.0
                
                for idx in nearest_indices:
                    # Get Gaussian parameters
                    mean = xyz[idx]
                    opacity = opacities[idx]
                    covariance = covariances[idx]
                    color = gaussian_colors[idx]
                    
                    # Compute difference vector
                    diff = pixel_point - mean
                    
                    # Compute Gaussian value
                    try:
                        inv_cov = torch.inverse(covariance)
                        mahal_dist = diff @ inv_cov @ diff
                        gaussian_value = torch.exp(-0.5 * mahal_dist) * opacity
                        
                        if gaussian_value > 1e-6:  # Only consider significant contributions
                            total_value += gaussian_value
                            weighted_color += gaussian_value * color
                            total_weight += gaussian_value
                    except:
                        # Handle singular covariance matrices
                        continue
                    
                # Store results
                if total_weight > 0:
                    colors[i, j] = weighted_color / total_weight
                else:
                    colors[i, j] = torch.zeros(3, device='cuda')
                
                processed_pixels += 1
                if processed_pixels % 100 == 0:
                    pbar.update(100)
        pbar.update(total_pixels - pbar.n)
        
        
    colors_np = colors.detach().cpu().numpy()
    # u_coords_np = u_coords.detach().cpu().numpy()
    # v_coords_np = v_coords.detach().cpu().numpy()
    
    colors_clipped = np.clip(colors_np, 0, 1)
    colors_uint8 = (colors_clipped * 255).astype(np.uint8)
    colors_image = Image.fromarray(colors_uint8, mode='RGB')
    colors_path = f"{save_path}_k{k_nearest}_colors.png"
    colors_image.save(colors_path)
    print(f"Slice saved to: {colors_path}")
    

def main():
    parser = argparse.ArgumentParser(description="Slice a Gaussian point cloud from a PLY file.")
    parser.add_argument('--ply', type=str, required=True, help='Path to input PLY file')
    parser.add_argument('--k_nearest', type=int, default=20, help='Number of nearest Gaussians per pixel')
    parser.add_argument('--resolution', type=int, nargs=2, default=[256, 256], metavar=('WIDTH', 'HEIGHT'), help='Resolution of the output image (width height)')
    parser.add_argument('--axis', type=str, choices=['x', 'y', 'z'], default='y', help='Axis to slice along')
    parser.add_argument('--coordinate', type=float, default=0.5, help='Coordinate value for the slice along the chosen axis')
    parser.add_argument('--sh_degree', type=int, default=3, help='Spherical harmonics degree')
    parser.add_argument('--save_path', type=str, default='.', help='Path prefix for saving the output image')

    args = parser.parse_args()

    slice_gaussian(
        ply_path=args.ply,
        sh_degree=args.sh_degree,
        axis=args.axis,
        coordinate=args.coordinate,
        resolution=tuple(args.resolution),
        k_nearest=args.k_nearest,
        save_path=args.save_path
    )

if __name__ == "__main__":
    main()