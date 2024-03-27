import odrive
from odrive.enums import *

from loguru import logger as log


class BLDC:
    def __init__(self, 
                 axis: object,
                 ) -> object:
        self.axis = axis 

        self.mode = CONTROL_MODE_VELOCITY_CONTROL

    def set_vel(self, vel: float) -> None:
        #if self.mode != CONTROL_MODE_VELOCITY_CONTROL:
        #self.set_mode(CONTROL_MODE_VELOCITY_CONTROL)

        self.axis.controller.input_vel = vel

    def set_pos(self, pos: float) -> None:
        ...

    def set_mode(self, mode) -> None:
        self.axis.controller.config.control_mode = mode

    def set_state(self, state) -> None:
        self.axis.requested_state = state

class ODriveAPI:
    def __init__(self, 
                 invertM0: bool = False,
                 invertM1: bool = False,
                 ) -> object:
        self.invertM0 = invertM0
        self.invertM1 = invertM1

        self.odrive = None
        self.connect()

        self.m0 = BLDC(self.odrive.axis0)
        self.m1 = BLDC(self.odrive.axis1)
        
    def connect(self) -> None:
        log.info('Connecting to ODrive...')
        self.odrive = odrive.find_any()
        log.success('ODrive connected!')    

    def start(self) -> None:
        self.m0.set_state(AXIS_STATE_CLOSED_LOOP_CONTROL)
        self.m0.set_mode(CONTROL_MODE_VELOCITY_CONTROL)
        #self.m1.set_state(AXIS_STATE_CLOSED_LOOP_CONTROL)
        log.success('Started succesfully!')

    def stop(self) -> None:
        self.m0.set_state(AXIS_STATE_IDLE)
        self.m0.set_vel(0)
        self.m1.set_state(AXIS_STATE_IDLE)
        log.success('Stopped succesfully!')


if __name__ == "__main__":
    odrv = ODriveAPI()
    odrv.m0.set_vel(0)
