import cam_control as cc
import servo_control as sc

########################## Variables for Adjusting #################################
### Robo Tripod/Servo ###
port = 'COM3'
baudrate = 19200  # default is 19200
timeout = 1.5  # default is 1.5
### Camera ###
image_saving_path = '../photo/'  # photo saving path, default is '../photo'
vfps = 10  # video fps, default is 10
pfps = 25  # photo saving rate, default is 25

servo = sc.setup(port=port, baudrate=baudrate, timeout=timeout)
# start new thread for servo control
t_servo = threading.Thread(target=)

# Start the camera for adjusting exposure time
expo = cc.cam_exposure()

# Ready the camera for correct exposure time in milisec
cam = cc.cam_setup(expo)
#cam = cc.cam_setup(10)
# Start live video feed and ready for photo taking
cc.cam_video(cam, 1, vfps=vfps, pfps=pfps, fp=image_saving_path)
#cc.cam_save(cam)

sc.close(servo)
