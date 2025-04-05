import odrive
from enum import Enum


class ODriveController:
    class AxisState(Enum):
        UNDEFINED                                = 0
        IDLE                                     = 1
        STARTUP_SEQUENCE                         = 2
        FULL_CALIBRATION_SEQUENCE                = 3
        MOTOR_CALIBRATION                        = 4
        ENCODER_INDEX_SEARCH                     = 6
        ENCODER_OFFSET_CALIBRATION               = 7
        CLOSED_LOOP_CONTROL                      = 8
        LOCKIN_SPIN                              = 9
        ENCODER_DIR_FIND                         = 10
        HOMING                                   = 11
        ENCODER_HALL_POLARITY_CALIBRATION        = 12
        ENCODER_HALL_PHASE_CALIBRATION           = 13

    def __init__(
            self,
            swap_axis:    bool = False,
            invert_left:  bool = False,
            invert_right: bool = False,
            ):
        self.__odrv = odrive.find_any()
        assert self.__odrv is not None, "ODrive not connected!"

        self.__right_axis = self.__odrv.axis0
        self.__left_axis  = self.__odrv.axis1

        if swap_axis:
            self.__right_axis, self.__left_axis = self.__left_axis, self.__right_axis

        self.__invert_left_mlp  = -1 if invert_left else 1
        self.__invert_right_mlp = -1 if invert_right else 1

        self.start(request=None, response=None)

    def reboot(self) -> None: 
        print("[ODriveController] Rebooting odrive...")
        self.__odrv.reboot()
        try:
            self.__odrv.start()
            print("[ODriveController] ODrive successfully reconnected...")

        except Exception as err:
            print(f'[ODriveController] Exception occured while reconnecting ODrive: {err}')

    def start(self) -> None:
        self.__left_axis.requested_state  = self.AxisState.CLOSED_LOOP_CONTROL.value
        self.__right_axis.requested_state = self.AxisState.CLOSED_LOOP_CONTROL.value

    def stop(self) -> None:
        self.__right_axis.requested_state = self.AxisState.IDLE.value
        self.__left_axis.requested_state  = self.AxisState.IDLE.value

    def set_left_velocity(self, vel: float):
        self.__left_axis.input_vel = float(vel) * self.__invert_left_mlp

    def set_right_velocity(self, vel: float):
        self.__right_axis.input_vel = float(vel) * self.__invert_right_mlp
