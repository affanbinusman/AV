# don't need any sd card on EV3 brick or any code on the brick. The ev3_dc python library directly send command to the EV3 brick.
# just need to connect the brick using bluetooth or usb.
# https://pypi.org/project/ev3-dc/
# https://ev3-dc.readthedocs.io/en/latest/examples_motor.html

# protocol=ev3.BLUETOOTH, host='00:16:53:48:8E:97'

import ev3_dc as ev3
from thread_task import Task, Repeated, Sleep
from time import sleep

import ev3_dc as ev3

with ev3.TwoWheelVehicle(
    0.01518,  # radius_wheel
    0.11495,  # tread
    protocol=ev3.BLUETOOTH, host='00:16:53:48:8E:97'
) as my_vehicle:
    parcours = (
        my_vehicle.drive_straight(0.5) + #0.5
        my_vehicle.drive_turn(120, 0.0)+
        my_vehicle.drive_straight(0.5) +
        my_vehicle.drive_turn(120, 0.0) +
        my_vehicle.drive_straight(0.5) +
        my_vehicle.drive_turn(120, 0.0)
    )
    parcours.start(thread=False)