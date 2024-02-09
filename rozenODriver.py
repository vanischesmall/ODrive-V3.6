import odrive
from odrive.enums import *


class ODrive:
    def __init__(self) -> object:
        self.odrv = odrive.find_any()
        self.axis = [self.odrv.axis0, self.odrv.axis1]
        self.controller = [self.odrv.axis0.controller, self.odrv.axis1.controller]
        self.state = [AXIS_STATE_IDLE, AXIS_STATE_IDLE]
        self.mode = [AXIS_STATE_POSITION_CONTROL, AXIS_STATE_POSITION_CONTROL]
        
    def set_state(self, state: int, axis_ind: int = -1) -> None:
        if axis_ind == -1:
            self.axis[0].required_state = state
            self.axis[1].required_state = state
        else:
            self.axis[axis_ind].required_state = state

    def set_mode(self, mode: int, axis_ind: int = -1) -> None:
        if axis_ind == -1:
            self.controller[0].required_state = state
            self.controller[1].required_state = state
        else:
            self.controller[axis_ind].required_state = state

    def check_mode(self, mode: int, axis_ind: int) -> bool:
        if axis_ind == -1:
            if self.mode[0] != state or self.mode[1] != state:
                return False
        else:
            if self.mode[axis_ind] != state: 
                return False
        return True            

    def set_velocity(self, velocity: float, axis_ind: int = -1) -> None:
        self.check_mode(CONTROL_MODE_VELOCITY_CONTROL, axis_ind)

        if axis_ind == -1:
            self.controller[0].input_vel = velocity
            self.controller[1].input_vel = velocity
        else:
            self.controller[axis_ind].input_vel = velocity

    def set_position(self, position: float, axis_ind: int = -1) -> None:
        self.check_mode(CONTROL_MODE_POSITION_CONTROL, axis_ind)

        if axis_ind == -1:
            self.controller[0].input_pos = position
            self.controller[1].input_pos = position
        else:
            self.controller[axis_ind].input_pos = position 
