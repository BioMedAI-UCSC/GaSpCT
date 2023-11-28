import pydicom
import numpy as np

slices = [pydicom.dcmread(f) for f in list_of_dicom_files]

num_slices = len(slices)
array_shape = list(slices[0].pixel_array.shape)
array_shape.append(num_slices) 

volume_array = np.zeros(array_shape)

for i, s in enumerate(slices):
    volume_array[:,:,i] = s.pixel_array

new_slices = pydicom.Dataset()
new_slices.Rows = array_shape[0] 
new_slices.Columns = array_shape[1]
new_slices.NumberOfFrames = array_shape[2]



