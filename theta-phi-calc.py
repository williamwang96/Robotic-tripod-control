import math
import numpy as np

kite_string_length = 30  # in meters, can be adjusted
kite_horizontal_distance = 5  # in meters, approximate horizontal distance between flying kite and robo tripod

degree_per_pixel = 62.1 / math.sqrt(1024 ** 2 + 1280 ** 2)
# center of the photo
xcenter = (1280 - 1) / 2 
ycenter = (1024 - 1) / 2

# reality coordinate system basis vectors, consider flying the kite in the field
# front (the direction that people face the kite) is x positive
# left to front is y positive, up towards sky is z positive
b1, b2, b3 = np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])


def get_kite_angles(xpos, ypos):
	'''Given the kite's x,y coordinates in the photo, return its true theta, phi angles in degrees
	Input xpos and ypos are based on origin as top left of the photo
	Assume xpos is horizontal, right positive
	and ypos is vertical, down positive in the photo
	This function treats left as x positive and up as y positive in the photo	
	'''

	# calculate theta and phi in the photo with respect to (wrt) the center of the photo
	# can be converted (+/-90) if needed
	# center is 0 for theta and 90 for phi
	# photo cartesian coordinate system set up same as the reality one for easy conversion (see above)
	xdis_to_center = xcenter - xpos
	kite_photo_theta = math.radians(xdis_to_center * degree_per_pixel)
	ydis_to_center = ycenter - ypos
	kite_photo_phi = math.radians(90 - (ydis_to_center * degree_per_pixel))

	# convert to cartesian coordinates in phoyo coor.sys. using coor. transformation formulas
	kite_photo_x = kite_string_length * math.sin(kite_photo_phi) * math.cos(kite_photo_theta)
	kite_photo_y = kite_string_length * math.sin(kite_photo_phi) * math.sin(kite_photo_theta)
	kite_photo_z = kite_string_length * math.cos(kite_photo_phi)
	kite_photo_cartesian = np.array([kite_photo_x, kite_photo_y, kite_photo_z]) # kite position in the photo in cartesian coor.

	# photo coor. basis vectors
	photo_basis = get_photo_coordinate_basis()
	# kite position in reality in cartesian coor.
	kite_real_cartesian = np.matmul(photo_basis, kite_photo_cartesian)
	# transform to spherical coor. to get theta and phi
	kite_real_theta = math.atan(kite_real_cartesian[1] / kite_real_cartesian[0])
	kite_real_theta = math.degrees(kite_real_theta)
	kite_real_phi = math.sqrt(kite_real_cartesian[0] ** 2 + kite_real_cartesian[1] ** 2) / kite_real_cartesian[2]
	kite_real_phi = math.atan(kite_real_phi)
	kite_real_phi = math.degrees(kite_real_phi)

	theta_phi = np.array([kite_real_theta, kite_real_phi])


def get_robo_tripod_angles():
	'''Return robo tripod's current theta, phi angles'''
	# TODO
	# need to look at return values of geekduino
	# or find a way to record the angle (i.e. update global var each time sending angles to robo)

def get_photo_coordinate_basis():
	'''Return cartesian coordinate basis of camera/photo space in terms of reality basis vectors
	'''
	# need robo tripod current theta,phi angles (pass in by args or use global var, prefer the latter)
	# need robo_start_theta and robo_start_phi (start position facing the front)
	robo_curr_theta = math.radians()? #TODO, wrt front facing the kite (front is 0)
	robo_curr_phi = math.radians()? #TODO, wrt up towards sky (up is 0)

	cb1x = math.sin(robo_curr_phi) * math.cos(robo_curr_theta)
	cb1y = math.sin(robo_curr_phi) * math.sin(robo_curr_theta)
	cb1z = math.cos(robo_curr_phi)
	cb1 = np.array([cb1x, cb1y, cb1z])

	cb2x = math.sin(robo_curr_phi) * math.cos(robo_curr_theta + math.pi/2)
	cb2y = math.sin(robo_curr_phi) * math.sin(robo_curr_theta + math.pi/2)
	cb2z = math.cos(robo_curr_phi)
	cb2 = np.array([cb2x, cb2y, cb2z])
	
	cb3x = math.sin(robo_curr_phi - math.pi/2) * math.cos(robo_curr_theta)
	cb3y = math.sin(robo_curr_phi - math.pi/2) * math.sin(robo_curr_theta)
	cb3z = math.cos(robo_curr_phi - math.pi/2)
	cb3 = np.array([cb3x, cb3y, cb3z])

	return np.array([cb1, cb2, cb3])