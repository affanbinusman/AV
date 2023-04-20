import ev3_dc as ev3
import time

# 360 turn
speed = 10
turn = 190
my_ev3 = ev3.EV3(protocol=ev3.USB) # init ev3

vehicle = ev3.TwoWheelVehicle( # setup drive controls
    0.01518,  # radius_wheel
    0.11495,  # tread
    ev3_obj=my_ev3
    )
vehicle.polarity_left = -1
vehicle.polarity_right = -1

vehicle.move(speed, turn)
time.sleep(10)

vehicle.stop()
