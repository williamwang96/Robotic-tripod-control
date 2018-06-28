from ximea import xiapi
from PIL import Image
import cv2
import threading
import time

expo = 10 # initial exposure time for camera, used in adjusting expo time
image_path



def cam_close(cam):

    cv2.destroyAllWindows()

    #stop data acquisition
    print('\nStopping acquisition...')
    cam.stop_acquisition()

    #stop communication
    cam.close_device()

    print('Done.\n')

def cam_exposure():
    '''
    Change given camera's exposure time (in miliseconds)
    Enter 'done' to finish adjusting
    '''
    global expo
    try:
        while True:
            cam = cam_setup(expo * 1000)
            cam_video(cam)
            expo_temp = input('Enter exposure time (in miliseconds): ')
            if not expo_temp.isnumeric():
                if expo_temp.lower() == 'done':
                    break
                else:
                    print('Numbers only')
                    pass
            expo = int(expo_temp)


    except EOFError:
        cam_close(cam)

    except xiapi.Xi_error: 
        # when done is entered, closing camera force quites video stream, causing an exception
        print('Done.')

def cam_video(cam):
    '''
    Start live video of the given camera
    Exits on CTRL+C
    '''
    img = xiapi.Image()
    try:
        print('Starting live transmission...')
        print('\nPress CTRL+C to enter new exposure time.\n')
        while True:
            t0 = time.time()
            #get data and pass them from camera to img
            cam.get_image(img)

            #create numpy array with data from camera. Dimensions of the array are 
            #determined by imgdataformat
            data = img.get_image_data_numpy()

            font = cv2.FONT_HERSHEY_SIMPLEX
            text = '{:5.5f}'.format((time.time() - t0)*1000)
            cv2.putText(
                data, text, (900,150), font, 4, (255, 255, 255), 2
                )            
            cv2.imshow('Camera Live Feed', data)

            cv2.waitKey(1)
            
    except KeyboardInterrupt:
        cam_close(cam)

    except xiapi.Xi_error:
        # When camera is not closed by this func, exception occurs
        print('Done.')

def cam_setup(expo):
    '''
    This function receives exposure time and sets up the camera ready for live feed
    '''
  
    #create instance for the connected camera
    cam = xiapi.Camera()

    #start communication
    print('Opening the camera...')
    cam.open_device()

    #settings
    cam.set_imgdataformat('XI_RGB24') # TODO which format do we want to use?
    cam.set_exposure(expo) # in milliseconds
    # want 25fps, maybe frame rate mode?
    # do we need 40ms or less exposure time?
    print('\nExposure was set to %i us' %cam.get_exposure())
    
    #start data acquisition
    print('\nStarting data acquisition...')
    cam.start_acquisition()

    return cam

def cam_save(cam):
    pass

def example(expo):
    #create instance for first connected camera 
    cam = xiapi.Camera()

    #start communication
    print('Opening first camera...')
    cam.open_device()

    #settings
    cam.set_exposure(expo)
    cam.set_imgdataformat('XI_RGB24') # TODO which format do we want to use?


    #create instance of Image to store image data and metadata
    img = xiapi.Image()

    #start data acquisition
    print('Starting data acquisition...')
    cam.start_acquisition()

    try:
        print('Starting video. Press CTRL+C to exit.')
        t0 = time.time()
        while True:
            #get data and pass them from camera to img
            cam.get_image(img)

            #create numpy array with data from camera. Dimensions of the array are 
            #determined by imgdataformat
            data = img.get_image_data_numpy()

            #show acquired image with time since the beginning of acquisition
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = '{:5.2f}'.format(time.time()-t0)
            cv2.putText(
                data, text, (900,150), font, 4, (255, 255, 255), 2
                )
            cv2.imshow('XiCAM example', data)

            cv2.waitKey(1)
            
    except KeyboardInterrupt:
        cv2.destroyAllWindows()

    #stop data acquisition
    print('Stopping acquisition...')
    cam.stop_acquisition()

    #stop communication
    cam.close_device()

    print('Done.')
    
if __name__ == '__main__':
    #cam = cam_setup()
    #cam_video(cam)
    #cam_exposure(cam)
    cam_exposure()

def stm():

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

