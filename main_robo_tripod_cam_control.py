import cam_control as cc

# variables for adjusting
image_saving_path = '../photo/'  # photo saving path, default is '../photo'
vfps = 10  # video fps, default is 10
pfps = 25  # photo saving rate, default is 25


# Start the camera for adjusting exposure time
expo = cc.cam_exposure()

# Ready the camera for correct exposure time in milisec
cam = cc.cam_setup(expo)
#cam = cc.cam_setup(10)
# Start live video feed and ready for photo taking
cc.cam_video(cam, 1, vfps=vfps, pfps=pfps, fp=image_saving_path)
#cc.cam_save(cam)
