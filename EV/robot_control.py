import torch
import numpy as np
import cv2 as cv
import ev3_dc as ev3
from thread_task import Sleep

# -------- INIT CONSTS --------

img_width = 1920
img_height = 1440
thresh = 0.3 # confidence threshold
centerline = 0.5 # value between 0 and 1 indicating the horizontal postition of vehicle center in the image
sweep_y_min = 0.9 # min y-value to be in range for removal
sweep_x_min = 0 # min x-value to be in range for removal
sweep_x_max = 1 # max x-value to be in range for removal
is_moving = False # indicates whether vehicle is moving
fwd_speed = 20 # vehicle movement fwd_speed
max_turn_speed = 100 # max turn speed

# ----- SETUP VEHICLE --------

my_ev3 = ev3.EV3(protocol=ev3.USB) # init ev3

vehicle = ev3.TwoWheelVehicle( # setup drive controls
    0.01518,  # radius_wheel
    0.11495,  # tread
    ev3_obj=my_ev3
    )
vehicle.polarity_left = -1
vehicle.polarity_right = -1

sweep_motor = ev3.Motor( # setup sweep motor
	ev3.PORT_B,
	ev3_obj = my_ev3
) 

sweep = ( # design sweep action
	sweep_motor.move_by(-60, speed = 100, brake=True) +
	Sleep(0.5) +
	sweep_motor.move_by(60, speed = 20, brake=True) +
	sweep_motor.stop_as_task(brake=False)
)

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
	
	# get detections
	det_all = results.xyxy[0].detach().numpy()
	
	# Show bounding boxes and labels on the current frame
	results.render()
	
	# return color to open-cv standard
	img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

	# Display the resulting frame
	cv.imshow('frame', img)
	
	# exit on command
	if cv.waitKey(1) == ord('q'):
		if is_moving:
			vehicle.stop()
			is_moving = False
		break
	
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
			if is_moving:
				vehicle.stop()
				is_moving = False
			
			# sweep arm to remove block
			sweep.start()
			sweep.join()
			sweep.stop()
	else:
		# no more blocks, stop drive motors
		if is_moving:
			vehicle.stop()
			is_moving = False
		continue
	
	# navigate to next brick with largest y-val (lowest in frame)
	if len(det_real) > 0:
		# calculate proportional turn radius
		lowest_idx = np.argmax(center_y)
		lowest_x = center_x[lowest_idx]
		turn = int((lowest_x - 0.5) * 2 * max_turn_speed)
		
		# move
		vehicle.move(fwd_speed, turn)
		is_moving = True
	else:
		# no more blocks, stop drive motors
		if is_moving:
			vehicle.stop()
			is_moving = False
		continue

# Release the capture and destroy the window
cap.release()
cv.destroyAllWindows()