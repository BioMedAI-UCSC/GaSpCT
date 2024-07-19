import os
import re

def extract_metrics(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    ssim = re.search(r'SSIM\s*:\s*([\d.]+)', content)
    psnr = re.search(r'PSNR\s*:\s*([\d.]+)', content)
    lpips = re.search(r'LPIPS\s*:\s*([\d.]+)', content)
    
    return [
        float(ssim.group(1)) if ssim else None,
        float(psnr.group(1)) if psnr else None,
        float(lpips.group(1)) if lpips else None
    ]

def find_metrics_files(root_dir):
    metrics_dict = {}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'ratio2' in dirpath and 'metrics.txt' in filenames:
            file_path = os.path.join(dirpath, 'metrics.txt')
            metrics = extract_metrics(file_path)
            if all(metrics):  # Ensure all metrics were found
                metrics_dict[dirpath] = metrics
    
    return metrics_dict

# Usage
root_directory = '/media/DATA_18_TB_2/manolis/GaSpCT/output'  # Replace with your root directory
metrics_dict = find_metrics_files(root_directory)

import pdb; pdb.set_trace()

print("Metrics dictionary:")
for path, metrics in metrics_dict.items():
    print(f"{path}: {metrics}")