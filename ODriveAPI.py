import odrive
from odrive.enums import AXIS_STATE_IDLE, AXIS_STATE_CLOSED_LOOP_CONTROL, CONTROL_MODE_VELOCITY_CONTROL

from loguru import logger as log
from time import time, sleep


class Acceleration:
    def __init__(self, accel=1):
        self.curr_vel = 0
        self.prev_vel = 0
        self.prev_tim = time()
        self.accel = accel

    def get_acceled_vel(self, target_velocity):
        delta = self.accel * (time() - self.prev_tim)
        
        if target_velocity > self.curr_vel:
            self.curr_vel = min(self.curr_vel + delta, target_velocity)
        elif target_velocity < self.curr_vel:
            self.curr_vel = max(self.curr_vel - delta, target_velocity)
        
        self.prev_tim = time() 
        return self.curr_vel

class ODriveAPI: 
    def __init__(self, 
                 invertM0: bool = False, 
                 invertM1: bool = False,
                 accel: float = None,
                 ) -> object:
        self.invertM0 = invertM0
        self.invertM1 = invertM1

        self.odrive = None
        self.is_connected = False

        self.connect()

        self.vel0 = 0
        self.vel1 = 0
        self.accelM0 = Acceleration(accel) if accel is not None else None
        self.accelM1 = Acceleration(accel) if accel is not None else None
    
    def connect(self) -> object:
        # log.info('Connecting to ODrive...')
        self.odrive = odrive.find_any()
        
        # log.success('Connected to ODrive!')
        self.is_connected = True
        return self.odrive
    
    def start(self) -> None:
        # log.info('Starting ODrive...')
        self.odrive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrive.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        self.odrive.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

    def stop(self) -> None:
        self.odrive.axis0.requested_state = AXIS_STATE_IDLE
        self.odrive.axis1.requested_state = AXIS_STATE_IDLE

    def brake(self) -> None:
        self.set_vel(0, 0)
        self.set_vel(1, 0)
        sleep(1)

    def set_vel(self, axis: int, vel: float) -> None:
        assert axis in [0, 1], 'Axis must be 0 or 1'

        if axis == 0:
            if self.odrive.axis0.controller.config.control_mode != CONTROL_MODE_VELOCITY_CONTROL:
                self.odrive.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
            if self.odrive.axis0.requested_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
                self.odrive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL


            self.vel0 = self.accelM0.get_acceled_vel(vel) if self.accelM0 is not None else vel
            self.odrive.axis0.controller.input_vel = self.vel0 * (-1 if self.invertM0 else 1)
        
        if axis == 1:
            if self.odrive.axis1.controller.config.control_mode != CONTROL_MODE_VELOCITY_CONTROL:
                self.odrive.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
            if self.odrive.axis1.requested_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
                self.odrive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

            self.vel1 = self.accelM1.get_acceled_vel(vel) if self.accelM1 is not None else vel
            self.odrive.axis0.controller.input_vel = self.vel1 * (-1 if self.invertM1 else 1)
    

if __name__ == '__main__':
    odrive = ODriveAPI()
    odrive.start()

    tmr = time()
    while time() - tmr < 10:
        odrive.set_vel(0, 2)
        odrive.set_vel(1, 2)
    odrive.stop() # free to move    