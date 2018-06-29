from ximea import xiapi
import cv2
import threading
import time
import os
import datetime

########################## Variables for Adjusting #################################
image_saving_path = '../photo/'  # photo saving path, default is '../photo', both relative and absolute work
#image_saving_path = 'C:/Users/William/Documents/project kite/photo/'
vfps = 10  # video fps, default is 10
pfps = 25  # photo saving rate, default is 25
expo = 10 # starting exposure time, in milisec


def cam_close(cam):
    '''
    Perform closing of the camera
    '''

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
            cam = cam_setup(expo)
            cam_video(cam, 0)
            expo_temp = input('Enter exposure time (in milisec) or done adjusting: ')
            if not expo_temp.isnumeric():
                if expo_temp.lower() == 'done':
                    break
                else:
                    print('Numbers only')
                    continue
            expo = int(expo_temp)


    except EOFError:
        cam_close(cam)

    except xiapi.Xi_error: 
        # when done is entered, closing camera force quites video stream, causing an exception
        print('Done.')

def cam_video(cam, mode, vfps=10, pfps=25, fp=image_saving_path):
    '''
    Start live video of the given camera
    Mode 0 is live video only
    Mode 1 starts to save photos
    video fps is unrestricted in mode 0
    vfps is used to set video fps, only effective in mode 1
    default vfps is 10
    pfps sets photo saving rate
    fp sets photo saving path in mode 1
    '''
    img = xiapi.Image()
    try:
        print('Starting live transmission...')
        if mode == 0: 
            print('\nPress CTRL+C to enter new exposure time or finish adjusting.\n')
        elif mode == 1:
            print('\nPress CTRL+C to quit')
            t_save = threading.Thread(target=cam_save, args=(cam, pfps, fp, ))
            t_save.start()
        else:
            print('Invalid init param')
        while True:
            # if taking photos, limit video fps
            if mode == 1:
                t0 = time.time()
            
            #get data and pass them from camera to img
            cam.get_image(img)

            #create numpy array with data from camera. Dimensions of the array are 
            #determined by imgdataformat
            data = img.get_image_data_numpy()

            # resize the display
            dim = (int(data.shape[1]/3), int(data.shape[0]/3))
            resized = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
            
            cv2.imshow('Camera Live Feed', resized)
            cv2.waitKey(1)

            if mode == 1:
                while time.time()-t0 < 1/vfps:
                    pass
            
    except KeyboardInterrupt:
        cam_close(cam)

    except xiapi.Xi_error:
        # When camera is not closed by this func, exception occurs
        print('Done.')

def cam_setup(expo=10):
    '''
    This function receives exposure time in milisec and sets up the camera ready for live feed
    '''
  
    #create instance for the connected camera
    cam = xiapi.Camera()

    #start communication
    print('Opening the camera...')
    cam.open_device()

    #settings
    cam.set_imgdataformat('XI_RGB24')
    cam.set_exposure(expo * 1000)
    print('\nExposure was set to %i us' %cam.get_exposure())
    
    #start data acquisition
    print('\nStarting data acquisition...')
    cam.start_acquisition()

    return cam

def cam_save(cam, fps=25, fp=image_saving_path):
    '''
    This function saves photo at most 40ms
    '''
    curr = 0

    print('\nReady... start taking photos')

    try:
        if not os.path.exists(os.path.dirname(image_saving_path)):
            os.makedirs(os.path.dirname(image_saving_path))
        while True:
            t0 = time.time()
            #print(curr)

            # get data from camera and ready for storing
            img = xiapi.Image()
            cam.get_image(img)
            t1 = time.time()
            data = img.get_image_data_numpy(invert_rgb_order=True)
            t2 = time.time()

            # generate filename
            filename = ("img%d_%s.bmp" % (curr, str(datetime.datetime.now()).split('.')[0].replace(" ",'-').replace(":",'-')))

            # save image
            cv2.imwrite(image_saving_path+filename, data)
            t3 = time.time()
            curr += 1    

            t3 = t3 - t2
            t2 = t2 - t1
            t1 = t1 - t0 

            print(str(int(t1*1000000)) + ' ' 
                    + str(int(t2*1000000)) + ' '
                    + str(int(t3*1000000)) + ' ' 
                    )

            while time.time()-t0 < 1/fps:
                # if not yet 40ms, wait
                pass        

    except KeyboardInterrupt:
        cam_close(cam)

def main():
    global expo

    # Start the camera for adjusting exposure time
    cam_exposure()

    # Ready the camera for correct exposure time in milisec
    cam = cam_setup(expo)
    
    # Start live video feed and ready for photo taking
    cam_video(cam, 1, vfps=vfps, pfps=pfps, fp=image_saving_path)


if __name__ == '__main__':
    main()

# TODO, currently provided by WIN10 console feature
# keyboard control for start taking photos
# pause taking photos
# exit program

