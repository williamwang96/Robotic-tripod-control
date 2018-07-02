from ximea import xiapi
import cv2
import threading
import time
import os
import datetime
import numpy as np

# Camera model: MQ013CG-E2

########################## Variables for Adjusting #################################

# photo saving path, default is '../photo', both relative and absolute work
# remember to add / to the end of the path if wanting to save in that folder
image_saving_path = '../photo/'  
#image_saving_path = 'C:/Users/William/Documents/project kite/photo/'

# starting exposure time when adjusting exposure, in milisec
expo = 10 


def get_key(img_key=np.array((0,0))):
    '''
    Function for receving keyboard input using opencv
    '''
    cv2.namedWindow('Camera Control', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Camera Control', 300, 150)
    
    cv2.imshow('Camera Control',img_key)
    k=cv2.waitKey(1)
    
    return k

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

    print('Camera Closed.')

def cam_live_video_original_resolution(cam):
    '''
    Start live video of the given camera, showing original resolution
    '''
    img = xiapi.Image()
    try:
        while True:
            #get data and pass them from camera to img
            cam.get_image(img)

            #create numpy array with data from camera. Dimensions of the array are 
            #determined by imgdataformat
            data = img.get_image_data_numpy()

            cv2.imshow('Camera Live Feed', data)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        cam_close(cam)

    except xiapi.Xi_error:
        # When camera is not closed by this func, exception occurs
        print('Camera Closed.')

def cam_adjust_exposure():
    '''
    Function for adjusting exposure time (in miliseconds) when starting the camera
    When prompt, enter new exposure time or press enter directly to finish adjusting
    '''
    global expo
    try:
        while True:
            cam = cam_setup(expo)

            print('\nPress CTRL+C to enter new exposure time or finish adjusting.\n')
            cam_live_video_original_resolution(cam)

            expo_temp = input('\nEnter exposure time (in milisec)\nOr press enter to finish: \n')

            if not expo_temp.isnumeric():
                if expo_temp == '':                    
                    break
                else:
                    print('Numbers only')
                    continue

            expo = int(expo_temp)

        print('Exposure time set.')

    except EOFError:
        pass

    except xiapi.Xi_error: 
        pass

    finally:
        print('\nDone.')

def cam_setup(expo=10):
    '''
    This function receives exposure time in milisec and sets up the camera ready for live feed
    '''
  
    #create instance for the connected camera
    cam = xiapi.Camera()

    #start communication
    print('\nOpening the camera...')
    cam.open_device()

    #settings
    cam.set_imgdataformat('XI_RGB24')
    cam.set_exposure(expo * 1000)
    print('\nExposure was set to %i us' %cam.get_exposure())
    
    #start data acquisition
    print('\nStarting data acquisition...')
    cam.start_acquisition()

    return cam

def cam_live_video_and_photo_save(cam, refrate=3, res=3, fp=image_saving_path):
    '''
    This function starts low-resolution live video and supports photo saving.
    Photo saving is controlled by keyboard inputs.
    Press R to start saving photos. Press P to pause saving. Press B to exit.
    refrate is the refreshing rate of the live video, taking positive integers, default is 3.
    Its value means showing one for every refrate photos in live video.
    res is the resolution of the live video, taking positive integers, default is 3. 
    Its value means reducing both the original width and height of the photo to 1/res, thus reducing
    the resolution to 1/res^2.
    '''
    curr = 0

    print('\nBegins live transmission...\nReady')
    print('Press R to start saving photos')
    print('Press P to pause')
    print('Press B to exit')

    try:
        # check whether given filepath exists
        # if not, create it
        if not os.path.exists(os.path.dirname(image_saving_path)):
            os.makedirs(os.path.dirname(image_saving_path))
        
        # boolean for deciding whether the camera needs to save photos
        save = False

        while True:
            t0 = time.time()

            # keyborad control
            k = get_key()

            if k == ord('r'):
                if not save:
                    save = True
                    print('\nStart saving photos\n')

            if k == ord('p'):
                if save:
                    save = False
                    print('\nPAUSED\n')
                    print('Press R to start saving photos')
                    print('Press P to pause')
                    print('Press B to exit')

            if k == ord('b'):
                break

            # get data from camera and ready for storing
            img = xiapi.Image()
            cam.get_image(img)
            t1 = time.time()

            data = img.get_image_data_numpy()
            t2 = time.time()
            
            # live video, showing a new photo every refrate ones
            if curr%refrate == 0:
                # resize the display, decrease resolution
                dim = (int(data.shape[1]/res), int(data.shape[0]/res))
                resized = cv2.resize(data, dim, interpolation=cv2.INTER_AREA)
                
                cv2.imshow('Camera Live Feed', resized)
                cv2.waitKey(1)

            # photo saving
            if save:
                # generate filename
                filename = ("img%d_%s.bmp" % (curr, str(datetime.datetime.now()).split('.')[0].replace(" ",'-').replace(":",'-')))
                # save image
                cv2.imwrite(image_saving_path+filename, data)

                t3 = time.time()            

                t3 = t3 - t2
                t2 = t2 - t1
                t1 = t1 - t0

                # Three time lengths are in units of microsecs
                # t1 is data acquisition time
                # t2 is data format transformation time
                # t3 is photo saving time
                # printing shows photo saving is happening
                print(str(int(t1*1000000)) + '  ' 
                        + str(int(t2*1000000)) + '  '
                        + str(int(t3*1000000)) + '  ' 
                        )

            curr += 1

    except KeyboardInterrupt:
        cam_close(cam)

    except xiapi.Xi_error: 
        pass

def cam_adjust_white_balance(cam):
    '''
    This function guides you to set the camera's white balance manually.
    '''
    global expo
    try:
        print('\nFace the camera towards a white paper or surface.\n' +
            'The camera will use it to set its white balance.\n' + 
            'Press CTRL+C when you are ready.')

        cam_live_video_original_resolution(cam)

        cam_wb = cam_setup(expo)

        cam_wb.set_param("manual_wb", 1)        

    except KeyboardInterrupt:
        pass

    except xiapi.Xi_error: 
        pass

    finally:
        print('White balance set.')

    return cam_wb


def main():
    global expo

    # Start the camera for adjusting exposure time
    cam_adjust_exposure()

    # Ready the camera for correct exposure time in milisec
    cam = cam_setup(33)

    # Adjusting the camera's white balance manually
    cam = cam_adjust_white_balance(cam)

    # Start live video feed and ready for photo taking
    cam_live_video_and_photo_save(cam)


if __name__ == '__main__':
    main()