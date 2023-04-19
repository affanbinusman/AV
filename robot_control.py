import torch
import numpy as np
import cv2 as cv
import ev3_dc as ev3
from thread_task import Task, Repeated, Sleep
from time import sleep

# -------- INIT CONSTS --------

img_width = 1920
img_height = 1440
thresh = 0.3 # confidence threshold
deadband = 0.1 # for left-right steering, maximum distance of block from image midline before steering kicks in
sweep_y_min = 0.8 # min y-value to be in range for removal
sweep_x_min = 0.3 # min x-value to be in range for removal
sweep_x_max = 0.7 # max x-value to be in range for removal
is_moving_left = 0 # flag = 1 indicates motor is moving
is_moving_right = 0 # flag = 1 indicates motor is moving

# ----- SETUP EV3 MOTORS --------

# # left side drive
# left = my_motor = ev3.Motor(
# 	ev3.PORT_D,
# 	protocol=ev3.USB
# )
# 
# # right side drive
# right = my_motor = ev3.Motor(
# 	ev3.PORT_A,
# 	protocol=ev3.USB
# )
# 
# # sweeper motor
# sweeper = my_motor = ev3.Motor(
# 	ev3.PORT_B,
# 	protocol=ev3.USB
# )

# -------- RUN ----------

# open camera, exit if not opening
cap = cv.VideoCapture(0,cv.CAP_ANY,(cv.CAP_PROP_FRAME_WIDTH,img_width,
									 cv.CAP_PROP_FRAME_HEIGHT,img_height))
if not cap.isOpened():
	print("Cannot open camera")
	exit()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'/Users/matt/Downloads/best (1).pt')

while True:
	# Capture frame-by-frame
	ret, img = cap.read()
	
	# Check if frame is read correctly, exit if not
	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break
	
	# convert img to RGB
	img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	
	# Run inference on the current frame
	results = model(img)
	
	# Show bounding boxes and labels on the current frame
	results.render()

    # Display the resulting frame
	cv.imshow('frame', img)
	
	sleep(1)
    
    # exit on command
	if cv.waitKey(1) == ord('q'):
		break
	
	# get detections
	det_all = results.xyxy[0].detach().numpy()
	
	# throw out detections with confidence < threshold
	keep_mask = det_all[:,4] > thresh
	det_real = det_all[keep_mask,:]
	
	# get x-val and y-val of bbox center point of all confident detections
	ul_y = det_real[:,1]
	lr_y = det_real[:,3]
	center_y = ((ul_y + lr_y) / 2) / img_height
	
	ul_x = det_real[:,0]
	lr_x = det_real[:,2]
	center_x = ((ul_x + lr_x) / 2) / img_width
	
	# determine if there is a "bad" block in position for removal
	if len(det_real) > 0:
		lowest_idx = np.argmax(center_y)
		lowest_y = center_y[lowest_idx]
		lowest_x = center_x[lowest_idx]
		lowest_cls = det_real[lowest_idx,5]
		if lowest_y >= sweep_y_min and lowest_x >= sweep_x_min and lowest_x <= sweep_x_max and lowest_cls != 1:
			# remove brick entries from detection and center arrays
			np.delete(center_y, lowest_idx, 0)
			np.delete(center_x, lowest_idx, 0)
			np.delete(det_real, lowest_idx, 0)
			
			# stop drive motors to sweep
	# 		left.stop()
	# 		is_moving_left = 0
	# 		right.stop()
	# 		is_moving_right = 0
			print("stopping to sweep")
			
			# --- sweep arm to remove block
			print("sweeping")
	else:
		# no more blocks, stop drive motors
		print("stopping")
		continue
	
	# navigate to next brick with largest y-val (lowest in frame)
	if len(det_real) > 0:
		lowest_idx = np.argmax(center_y)
		lowest_x = center_x[lowest_idx]
		if lowest_x < 0.5 - deadband: # brick is to the left of the deadband
	# 		if is_moving_right:
	# 			right.stop()
	# 			is_moving_right = 0
	# 		if not is_moving_left:
	# 			left.start_move()
	# 			is_moving_left = 1
			print("turning left")
		elif lowest_x > 0.5 + deadband: # brick is to the right of the deadband
	# 		if is_moving_left:
	# 			left.stop()
	# 			is_moving_left= 0
	# 		if not is_moving_left:
	# 			left.start_move()
	# 			is_moving_left = 1
		print("turning right")
		else: # brick is straight ahead
			# --- turn both drive motors
			print("driving straight")
	else:
		# no more blocks, stop drive motors
		print("stopping")
		continue

# Release the capture and destroy the window
cap.release()
cv.destroyAllWindows()