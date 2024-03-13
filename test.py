import odrive
from odrive.enums import *

from time import sleep

odrv = odrive.find_any()
print('find')
odrv.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
odrv.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

odrv.axis0.controller.input_vel = -1
odrv.axis1.controller.input_vel = -1
sleep(5)
odrv.axis0.controller.input_vel = 1 
odrv.axis1.controller.input_vel = 1 
sleep(5)
odrv.axis0.requested_state = AXIS_STATE_IDLE
odrv.axis1.requested_state = AXIS_STATE_IDLE
