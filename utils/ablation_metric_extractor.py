import os
import re
from collections import defaultdict
import time

def extract_metrics(file_path):
    try:
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
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return [None, None, None]

def extract_config(path):
    match = re.search(r'ltv([\d.]+)_lb([\d.]+)_ellipsoid(\d+)', path)
    if match:
        return f"ltv{match.group(1)}_lb{match.group(2)}_ellipsoid{match.group(3)}"
    return None

def find_metrics_files(root_dir):
    metrics_dict = {}
    start_time = time.time()
    file_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=False):
        if time.time() - start_time > 5:  # Print progress every 5 seconds
            print(f"Processed {file_count} files so far...")
            start_time = time.time()
        
        if 'ratio2' in dirpath and 'metrics.txt' in filenames:
            file_path = os.path.join(dirpath, 'metrics.txt')
            metrics = extract_metrics(file_path)
            if all(metrics):  # Ensure all metrics were found
                metrics_dict[dirpath] = metrics
        
        file_count += len(filenames)
    
    return metrics_dict

def group_by_config(metrics_dict):
    config_dict = defaultdict(list)
    for path, metrics in metrics_dict.items():
        config = extract_config(path)
        if config:
            config_dict[config].append(metrics)
    
    avg_metrics = {}
    for config, metrics_list in config_dict.items():
        avg_metrics[config] = [
            sum(metric[i] for metric in metrics_list) / len(metrics_list)
            for i in range(3)
        ]
    
    return avg_metrics

# Usage
root_directory = '/media/DATA_18_TB_2/manolis/GaSpCT/output'  # Replace with your root directory
print("Starting to search for metrics files...")
metrics_dict = find_metrics_files(root_directory)
print(f"Found {len(metrics_dict)} metrics files.")

print("Grouping metrics by configuration...")
avg_metrics_by_config = group_by_config(metrics_dict)

print("Average metrics by configuration:")
for config, avg_metrics in avg_metrics_by_config.items():
    print(f"{config}: SSIM={avg_metrics[0]:.4f}, PSNR={avg_metrics[1]:.4f}, LPIPS={avg_metrics[2]:.4f}")