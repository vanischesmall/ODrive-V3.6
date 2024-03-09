import odrive
from odrive.enums import *

from loguru import logger as log
from time import time, sleep


class ODriveAPI: 
    def __init__(self, 
                 invertM0: bool = False, 
                 invertM1: bool = False,
                 ) -> object:
        self.invertM0 = invertM0
        self.invertM1 = invertM1

        self.odrive = None
        self.is_connected = False

        self.connect()

        self.vel1 = None
        self.vel1_ = None
        self.vel_tmr1 = time()
        self.accel_tim1 = 0.1

        self.vel2 = None
        self.vel2_ = None
        self.vel_tmr2 = time()
        self.accel_tim2 = 0.1
    
    def connect(self) -> object:
        log.info('Connecting to ODrive...')
        self.odrive = odrive.find_any()
        
        log.success('Connected to ODrive')
        self.is_connected = True
        return self.odrive
    
    def start(self) -> None:
        log.info('Starting ODrive...')
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
            
            if self.vel1 != vel:
                delta = (time() - self.vel_tmr1) / self.accel_tim1
                
                if self.vel1 < vel:
                    self.vel1_ += delta
                else:
                    self.vel1_ -= delta
            else:
                self.vel_tmr1 = time()

            self.vel1 = vel
            self.vel1_ *= (-1 if self.invertM0 else 1)
            self.odrive.axis0.controller.input_vel = self.vel1_
            return self.vel1_
        
        if axis == 1:
            if self.odrive.axis1.controller.config.control_mode != CONTROL_MODE_VELOCITY_CONTROL:
                self.odrive.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
            
            if self.vel2 != vel:
                delta = (time() - self.vel_tmr2) / self.accel_tim2
                
                if self.vel2 < vel:
                    self.vel2_ += delta
                else:
                    self.vel2_ -= delta
            else:
                self.vel_tmr2 = time()
                
            self.vel2 = vel
            self.vel2_ *= (-1 if self.invertM1 else 1)
            self.odrive.axis0.controller.input_vel = self.vel2_ 
            return self.vel2_


if __name__ == '__main__':
    odrive = ODriveAPI()
    odrive.start()

    tmr = time()
    while time() - tmr < 10:
        odrive.set_vel(0, 2)
        odrive.set_vel(1, 2)
    
    odrive.brake()
    odrive.stop()