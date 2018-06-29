import cam_control as cc

# Start the camera for exposure time setting
#expo = cc.cam_exposure()

# Ready the camera for correct exposure time in milisec and start live feed
cam = cc.cam_setup(1)
cc.cam_video(cam, 1)
#cc.cam_save(cam)
