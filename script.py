import odrive
from odrive.enums import *

from time import sleep


def move0(odrv, vel):
    odrv.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv.axis0.controller.input_vel = vel

def move1(odrv, vel):
    odrv.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    odrv.axis1.controller.input_vel = vel

class Controller:
    def __init__(self, controller):
        self.controller = controller

    def move(self, vel):
        self.controller.input_vel = vel

    def stop(self):
        self.controller.input_vel = 0 



if __name__ == "__main__":
    odrv0 = odrive.find_any()

    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    controller0 = Controller(odrv0.axis0.controller)
    controller1 = Controller(odrv0.axis1.controller)
        
    while True:
        try:
            controller0.move(-1)
            controller1.move(1)
            sleep(4)

            controller0.stop()
            controller1.stop()
            sleep(2)

            controller0.move(1)
            controller1.move(-1)
            sleep(4)

            controller0.stop()
            controller1.stop()
            sleep(2)

            
        except KeyboardInterrupt:
            odrv0.axis0.requested_state = AXIS_STATE_IDLE
            odrv0.axis1.requested_state = AXIS_STATE_IDLE
            break
