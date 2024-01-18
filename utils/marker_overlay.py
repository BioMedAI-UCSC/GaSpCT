import pydicom  
import pdb

img1_name = "test1.dcm"
img2_name = "test2.dcm"
output_name = "overlay_out2.dcm"

img1 = pydicom.dcmread(img1_name)  
img2 = pydicom.dcmread(img2_name)
img_out = pydicom.dcmread(img2_name)



pixel_array = img1.pixel_array
# Print dimensions  
print(f"Width: {pixel_array.shape[1]}")
print(f"Height: {pixel_array.shape[0]}")

pixel_array2 = img2.pixel_array
# Print dimensions  
print(f"Width: {pixel_array2.shape[1]}")
print(f"Height: {pixel_array2.shape[0]}")

overlay_start_x = 100  
overlay_start_y = 100
overlay_end_x = 400
overlay_end_y = 400

# Store pixel array  
pixels = img1.pixel_array


overlay_data = pixels[overlay_start_y:overlay_end_y,overlay_start_x:overlay_end_x] 

#img2.pixel_array[overlay_start_y:overlay_end_y,overlay_start_x:overlay_end_x]

#print(f"Shape: {pixels[overlay_start_y:overlay_end_y,overlay_start_x:overlay_end_x].shape}")
#print(f"Shape: {overlay_data.shape}")
print(f"Img2 Original: {img2.pixel_array[250,350]}")	

img2.pixel_array[overlay_start_y:overlay_end_y,  
                 overlay_start_x:overlay_end_x] = 0


img2.PixelData = img2.pixel_array.tobytes()

# img2.pixel_array[:, :] = 0 # set whole image to black 

print(f"Img1: {img1.pixel_array[250,350]}")
print(f"Img2 Altered: {img2.pixel_array[250,350]}")


# Save as new DICOM file
# pydicom.dcmwrite(output_name, img2)
img2.save_as(output_name)
again = pydicom.dcmread(output_name)

print(f"Again: {again.pixel_array[250,350]}")
