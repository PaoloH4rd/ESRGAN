import os
import glob
import nrrd
import cv2
import numpy as np

# Configuration
input_dir = 'LR'
output_dir = 'downscale'
scale_factor = 0.05  # Downscale to 5% of original size

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"Downscaling NRRD files from {input_dir} to {output_dir}...")

nrrd_files = glob.glob(os.path.join(input_dir, '*.nrrd'))

if not nrrd_files:
    print("No NRRD files found in LR/ folder.")

for path in nrrd_files:
    base_name = os.path.basename(path)
    output_path = os.path.join(output_dir, base_name)
    
    print(f"Processing {base_name}...")
    
    # Read NRRD
    data, header = nrrd.read(path)
    
    # Calculate new dimensions
    # NRRD data is often (H, W) or (W, H). pynrrd reads it such that 
    # we should check the shape.
    height, width = data.shape[:2]
    new_size = (int(width * scale_factor), int(height * scale_factor))
    
    # Resize using OpenCV (handles float/uint16/uint8)
    # Note: cv2.resize expects (width, height)
    resized_data = cv2.resize(data, new_size, interpolation=cv2.INTER_AREA)
    
    # Update header if necessary (simple copy usually works for basic resizing)
    new_header = header.copy()
    # Remove or update space directions if they exist to keep metadata clean
    if 'space directions' in new_header:
        del new_header['space directions']
    
    # Save as NRRD in the downscale folder
    nrrd.write(output_path, resized_data, new_header)
    print(f"Saved to {output_path} (New size: {resized_data.shape})")

print("Downscaling complete.")
