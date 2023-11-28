import pydicom  

img1 = pydicom.dcmread("image1.dcm")  
img2 = pydicom.dcmread("image2.dcm")

overlay_start_x = 200  
overlay_start_y = 300
overlay_end_x = 300   
overlay_end_y = 400

overlay_data = img1.pixel_array[overlay_start_y:overlay_end_y, 
                                overlay_start_x:overlay_end_x] 

img2.pixel_array[overlay_start_y:overlay_end_y,  
                 overlay_start_x:overlay_end_x] = overlay_data  

pydicom.dcmwrite("overlaid_image.dcm", img2)