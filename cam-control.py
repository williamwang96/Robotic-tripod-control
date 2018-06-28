from ximea import xiapi
from PIL import Image
import cv2

#create instance for the connected camera
cam = xiapi.Camera()

#start communication
print('Opening the camera...')
cam.open_device()

#settings
cam.set_imgdataformat('XI_RGB24') # TODO which format do we want to use?
# TODO
# make live video for tuning the camera
# prompt for exposure
cam.set_exposure(10000) # in milliseconds
# want 25fps, maybe frame rate mode?
# do we need 40ms or less exposure time?
print('Exposure was set to %i us' %cam.get_exposure())

#create instance of Image to store image data and metadata
img = xiapi.Image()

#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()


# TODO 
# change to live video
# save one image every 40ms
for i in range(10):
    # TODO
    # add timer for 40ms

    #get data and pass them from camera to img
    cam.get_image(img)

    #create numpy array with data from camera. Dimensions of array are determined
    #by imgdataformat
    #NOTE: PIL takes RGB bytes in opposite order, so invert_rgb_order is True
    data = img.get_image_data_numpy(invert_rgb_order=True)

    # TODO
    # add specific path for saving
    # use image_path variable and glob
    img = PIL.Image.fromarray(data, 'RGB') 
    img.save('xi_example.bmp')

    # TODO
    # keyboard control for start taking photos
    # pause taking photos
    # exit program

    

#stop data acquisition
print('Stopping acquisition...')
cam.stop_acquisition()

#stop communication
cam.close_device()

print('Done.')