from time import sleep
import ev3_dc as ev3
from thread_task import Sleep

with ev3.Motor(
    ev3.PORT_B,
    protocol=ev3.USB
) as my_motor:
    movement_plan = (
        my_motor.move_by(-60, speed = 100, brake=True) +
        Sleep(0.5) +
        my_motor.move_by(60, speed = 20, brake=True) +
        my_motor.stop_as_task(brake=False)
)

    movement_plan.start()
    print('movement has been started')
    movement_plan.join()
    print('movement has been finished')
    movement_plan.stop()