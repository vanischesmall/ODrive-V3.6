import odrive
from odrive.enums import *


class rozenODriver:
    def __init__(self) -> object:
        self.odrv = odrive.find_any()
        self.axis = (self.odrv.axis0, self.odrv.axis1)
        self.controller = [self.odrv.axis0.controller, self.odrv.axis1.controller]
        self.state = [AXIS_STATE_IDLE, AXIS_STATE_IDLE]
        self.mode = [CONTROL_MODE_VELOCITY_CONTROL, CONTROL_MODE_VELOCITY_CONTROL]

    def set_state(self, state: int, axis_ind: int = -1) -> None:
        if axis_ind == -1:
            self.axis[0].requested_state = state
            self.axis[1].requested_state = state
        else:
            self.axis[axis_ind].requested_state = state

    def set_mode(self, mode: int, axis_ind: int = -1) -> None:
        if axis_ind == -1:
            self.controller[0].config.control_mode = mode
            self.controller[1].config.control_mode = mode
        else:
            self.controller[axis_ind].config.control_mode = mode

    def check_mode(self, mode: int, axis_ind: int) -> bool:
        if axis_ind == -1:
            if self.mode[0] != mode or self.mode[1] != mode:
                return False
        else:
            if self.mode[axis_ind] != mode: 
                return False
        return True     

    def set_velocity(self, velocity: float | tuple[float, float], axis_ind: int = -1) -> None:
        if not self.check_mode(CONTROL_MODE_VELOCITY_CONTROL, axis_ind):
            self.set_mode(CONTROL_MODE_VELOCITY_CONTROL, axis_ind)

        if axis_ind == -1:
            if type(velocity) == float or type(velocity) == int:
                self.controller[0].input_vel = velocity
                self.controller[1].input_vel = velocity
            else:
                self.controller[0].input_vel = velocity[0]
                self.controller[0].input_vel = velocity[1]
        else:
            self.controller[axis_ind].input_vel = velocity

    def set_position(self, position: float | tuple[float, float], axis_ind: int = -1) -> None:
        if not self.check_mode(CONTROL_MODE_POSITION_CONTROL, axis_ind):
            self.set_mode(CONTROL_MODE_POSITION_CONTROL, axis_ind)

        if axis_ind == -1:
            if type(position) == float:
                self.controller[0].input_pos = position
                self.controller[1].input_pos = position
            else:
                self.controller[0].input_pos = position[0]
                self.controller[1].input_pos = position[1]
        else:
            self.controller[axis_ind].input_pos = position 

    def get_position(self, axis_ind: int = -1) -> tuple[float, float]:
        ...

    def stop(self, axis_ind: int = -1) -> None:
        self.set_state(AXIS_STATE_IDLE)
        self.set_velocity(0)
