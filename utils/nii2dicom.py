import os
import glob
import nibabel as nib
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import generate_uid
import datetime
import numpy as np
from pathlib import Path
import argparse

def create_basic_dicom_dataset(pixel_array, study_id, slice_number, total_slices, series_uid, study_uid, slice_thickness, image_position):
    """Creates a basic DICOM dataset with minimal required tags"""
    # Create file meta information
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # CT Image Storage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    # Create dataset
    ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
    
    # Add required DICOM tags
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.StudyInstanceUID = study_uid
    ds.SeriesInstanceUID = series_uid
    
    # Patient information
    ds.PatientName = f"NIFTI_{study_id}"
    ds.PatientID = study_id
    ds.PatientBirthDate = ''
    
    # Study information
    ds.StudyID = study_id
    ds.StudyDate = datetime.datetime.now().strftime('%Y%m%d')
    ds.StudyTime = datetime.datetime.now().strftime('%H%M%S')
    ds.AccessionNumber = ''
    
    # Series information
    ds.SeriesNumber = 1
    ds.InstanceNumber = slice_number + 1
    
    # Spatial positioning info
    ds.ImagePositionPatient = image_position
    ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]  # Axial orientation
    ds.PixelSpacing = [1, 1]  # Default to 1mm spacing if not available
    ds.SliceThickness = slice_thickness
    ds.SliceLocation = image_position[2]  # Z-coordinate
    
    # Image information
    ds.Rows = pixel_array.shape[0]
    ds.Columns = pixel_array.shape[1]
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 0
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    
    # Set the correct rescale values for CT
    ds.RescaleIntercept = -1024.0
    ds.RescaleSlope = 1.0
    ds.RescaleType = "HU"
    
    # Convert to uint16 and scale if necessary
    ds.PixelData = pixel_array.astype(np.uint16).tobytes()
    
    return ds

def convert_nifti_to_dicom(nifti_path, output_dir):
    """Converts a NIfTI file to a series of DICOM slices"""
    # Load the NIfTI file
    nifti_img = nib.load(nifti_path)
    nifti_data = nifti_img.get_fdata()
    
    # Get spatial information from NIfTI header
    pixel_dims = nifti_img.header.get_zooms()
    slice_thickness = float(pixel_dims[2]) if len(pixel_dims) > 2 else 1.0
    
    # Extract study ID from filename
    study_id = Path(nifti_path).stem.split('-')[0]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate UIDs once for the entire series
    series_uid = generate_uid()
    study_uid = generate_uid()
    
    # Get the number of slices
    total_slices = nifti_data.shape[2]
    
    # Convert each slice
    for slice_num in range(total_slices):
        # Extract the slice
        slice_data = nifti_data[:, :, slice_num]
        
        # Calculate the physical position of this slice
        image_position = [0, 0, slice_num * slice_thickness]
        
        # Normalize to 0-4095 range for CT
        slice_min = slice_data.min()
        slice_max = slice_data.max()
        slice_data = ((slice_data - slice_min) / (slice_max - slice_min) * 4095).astype(np.uint16)
        
        # Create DICOM dataset with consistent series and study UIDs
        ds = create_basic_dicom_dataset(
            slice_data, 
            study_id, 
            slice_num, 
            total_slices, 
            series_uid, 
            study_uid,
            slice_thickness,
            image_position
        )
        
        # Create output filename
        output_filename = f"{study_id}_slice_{slice_num:04d}.dcm"
        output_path = os.path.join(output_dir, output_filename)
        
        # Save the DICOM file
        ds.save_as(output_path)

def main():
    parser = argparse.ArgumentParser(description='Convert NIFTI files to DICOM slices')
    parser.add_argument('input_dir', help='Directory containing .nii.gz files')
    parser.add_argument('output_dir', help='Directory where DICOM files will be saved')
    args = parser.parse_args()

    # Find all .nii.gz files
    nifti_files = glob.glob(os.path.join(args.input_dir, "*.nii.gz"))
    
    # Create main output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    for nifti_file in nifti_files:
        # Create output directory name based on the NIfTI filename
        output_dirname = Path(nifti_file).stem.split('-')[0]
        output_dir = os.path.join(args.output_dir, output_dirname)
        
        print(f"Converting {nifti_file} to DICOM...")
        convert_nifti_to_dicom(nifti_file, output_dir)
        print(f"Conversion complete. DICOM files saved in {output_dir}")

if __name__ == "__main__":
    main()