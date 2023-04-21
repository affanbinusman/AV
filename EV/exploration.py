import ev3_dc as ev3
import time
import numpy as np
import time
import cv2 as cv

is_moving = False # indicates whether vehicle is moving
fwd_speed = 20 # vehicle movement fwd_speed
search_speed = 10 # speed during search

explore_turn = list(range(-200,200+1)) # spin in place during exploration 
len_explore_turn = len(explore_turn)
exploreFlag = False

my_ev3 = ev3.EV3(protocol=ev3.USB) # init ev3
vehicle = ev3.TwoWheelVehicle( # setup drive controls
    0.01518,  # radius_wheel
    0.11495,  # tread
    ev3_obj=my_ev3
    )

######
def explore():
    turn = explore_turn[np.random.randint(0,len_explore_turn)]
    turnFreq = np.random.randint(0,2)
    if turnFreq == 0:            # 50% turning
        vehicle.move(search_speed, turn)
        time.sleep(np.random.randint(1,5))
    else:         
    # 50% moving foward
        vehicle.move(fwd_speed, 0)
        time.sleep(np.random.randint(3,9))
        is_moving = True

    # else: 

# vehicle.move(10,0)
# time.sleep(3)
# vehicle.stop()
# exit()

while True:
    if cv.waitKey(1) == ord('q'):
        if is_moving:
            vehicle.stop()
            is_moving = False
        break

    print("came in while")
    # explore()
    print("exited explore()")
    