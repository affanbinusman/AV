from time import sleep
import ev3_dc as ev3
from thread_task import Sleep

#don't need any sd card on EV3 brick or any code on the brick. The ev3_dc python library directly send command to the EV3 brick.
# just need to connect the brick using bluetooth or usb.
# https://pypi.org/project/ev3-dc/
# https://ev3-dc.readthedocs.io/en/latest/examples_motor.html

with ev3.Motor(
    ev3.PORT_A,
    protocol=ev3.BLUETOOTH, host='00:16:53:48:8E:97'
) as my_motor:
    movement_plan = (
        my_motor.move_to(360) +
        Sleep(5) +
        my_motor.move_to(0, speed=100, ramp_up=90, ramp_down=90, brake=True) +
        Sleep(0.5) +
        my_motor.stop_as_task(brake=False)
    )

    movement_plan.start()
    print('movement has been started')

    movement_plan.join()
    print('movement has been finished')