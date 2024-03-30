import odrive
from odrive.enums import *

from loguru import logger as log

class Encoder:
    def __init__(self,
                 mode: int = ENCODER_MODE_HALL, 
                 bandwidth: int = 100,
                 cpr: int = 90):
        self.MODE = mode 
        self.BANDWIDTH = bandwidth
        self.CPR = cpr

class BLDC:
    def __init__(self, 
                 axis, 
                 invert: bool = False,
                 encoder: Encoder = Encoder(),
                 pole_pairs: int = 15,
                 kv: int = 16,
                 resistance_calib_max_voltage: float = 4.0,
                 requested_current_range: float = 25.0,
                 current_control_bandwidth: int = 100,
                 calibration_current: float = 5.0,
                 pos_gain: float = 1.0,
                 vel_gain: float = 0.02,
                 vel_integrator_gain: float = 0.1,
                 vel_limit: float = 15,
                 ) -> object:
        self.axis = axis 
        self.enc: Encoder = encoder
        self.invert_mlp = 1 if not invert else -1 # Invert multiplier

        # SOME CONSTANTS
        self.POLE_PAIRS = pole_pairs
        self.KV = kv
        self.RESISTANCE_CALIB_MAX_VOLTAGE = resistance_calib_max_voltage
        self.REQUESTED_CURRENT_RANGE = requested_current_range
        self.CURRENT_CONTROL_BANDWIDTH = current_control_bandwidth
        self.TORQUE_CONSTANT = 8.27 * self.KV
        self.CALIBRATION_CURRENT = calibration_current
        self.VEL_LIMIT = vel_limit
        self.POS_GAIN = pos_gain
        self.VEL_GAIN = vel_gain * self.TORQUE_CONSTANT * encoder.CPR
        self.VEL_INTEGRATOR_GAIN = vel_integrator_gain * self.TORQUE_CONSTANT * enc.CPR

        self.mode = None
        self.state = None

    def set_vel(self, vel: float) -> None:
        if self.mode != CONTROL_MODE_VELOCITY_CONTROL:
            self.mode = CONTROL_MODE_VELOCITY_CONTROL
            self.axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL

        self.axis.controller.input_vel = vel * self.invert_mlp

    def set_pos(self, pos: float) -> None:
        if self.mode != CONTROL_MODE_POSITION_CONTROL:
            self.mode = CONTROL_MODE_POSITION_CONTROL
            self.axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
            
        self.axis.controller.input_pos = pos * self.invert_mlp

    def set_mode(self, mode) -> None:
        if self.mode != mode:
            self.mode = mode
            self.axis.controller.config.control_mode = mode

    def set_state(self, state) -> None:
        if self.state != state:
            self.state = state
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

        self.m0 = BLDC(self.odrive.axis0, self.invertM0)
        self.m1 = BLDC(self.odrive.axis1, self.invertM1)
        
    def connect(self) -> None:
        log.info('Connecting to ODrive...')
        self.odrive = odrive.find_any()
        log.success('ODrive connected!')    

    def reboot(self) -> None:
        log.info('Rebooting...')
        self.odrive.reboot()
        while True:
            try:
                self.odrive.start()
                log.success('Reconnected successfully!')
                break;

            except:
                pass

        log.info('Done')

    def save_cfg(self) -> None:
        log.info('Saving configuration...')
        self.odrive.save_configuration()
        log.info('Done')

    def erase_cfg(self) -> None:
        log.info('Erasing configuration')
        self.odrive.erase_configuration()
        log.info('Done')

    def configure(self) -> None:
        self.erase_cfg()
        log.warn("Starting configuration ODrive!..")

        axis_ind = input('\n\nEnter axis index or press enter and configure two in line [0/1]')
        if axis_ind not in [0, 1]:
            axis_ind = 2

        if axis_ind == 0 or axis_ind == 2:
            self.m0.motor.config.pole_pairs = self.m0.POLE_PAIRS
            self.m0.motor.config.resistance_calib_max_voltage = self.m0.RESISTANCE_CALIB_MAX_VOLTAGE
            self.m0.motor.config.requested_current_range = self.m0.REQUESTED_CURRENT_RANGE
            self.m0.motor.config.current_control_bandwidth = self.m0.REQUESTED_CURRENT_RANGE
            self.m0.motor.config.torque_constant = self.m0.TORQUE_CONSTANT
            self.m0.motor.config.calibration_current = self.m0.CALIBRATION_CURRENT
            self.m0.motor.config.vel_limit = self.m0.VEL_LIMIT

            self.m0.encoder.config.mode = self.m0.enc.ENCODER_MODE_HALL
            self.m0.encoder.config.bandwidth = self.m0.enc.BANDWIDTH
            self.m0.encoder.config.cpr = self.m0.enc.CPR
            
            self.m0.controller.config.pos_gain = self.m0.POS_GAIN
            self.m0.controller.config.vel_gain = self.m0.VEL_GAIN
            self.m0.controller.config.vel_integrator_gain = self.m0.VEL_INTEGRATOR_GAIN

            self.save_cfg()
            self.reboot()
            
            input('\nBe sure M0 can move free and press enter to start calibration sequence')
            self.m0.set_state(AXIS_STATE_FULL_CALIBRATION_SEQUENCE)
            input('\nPress enter when u heared <beep> and motor cw and ccw')

            self.stop()
            self.m0.motor.config.pre_calibrated = True
            self.m0.encoder.config.pre_calibrated = True 

            self.save_cfg()
            self.reboot()
        
        if axis_ind == 1 or axis_ind == 2:
            self.m1.motor.config.pole_pairs = self.m1.POLE_PAIRS
            self.m1.motor.config.resistance_calib_max_voltage = self.m1.RESISTANCE_CALIB_MAX_VOLTAGE
            self.m1.motor.config.requested_current_range = self.m1.REQUESTED_CURRENT_RANGE
            self.m1.motor.config.current_control_bandwidth = self.m1.REQUESTED_CURRENT_RANGE
            self.m1.motor.config.torque_constant = self.m1.TORQUE_CONSTANT
            self.m1.motor.config.calibration_current = self.m1.CALIBRATION_CURRENT
            self.m1.motor.config.vel_limit = self.m1.VEL_LIMIT

            self.m1.encoder.config.mode = self.m1.enc.ENCODER_MODE_HALL
            self.m1.encoder.config.bandwidth = self.m1.enc.BANDWIDTH
            self.m1.encoder.config.cpr = self.m1.enc.CPR
    
            self.m1.controller.config.pos_gain = self.m1.POS_GAIN
            self.m1.controller.config.vel_gain = self.m1.VEL_GAIN
            self.m1.controller.config.vel_integrator_gain = self.m1.VEL_INTEGRATOR_GAIN

            self.save_cfg()
            self.reboot()
            
            input('\nBe sure M0 can move free and press enter to start calibration sequence')
            self.m1.set_state(AXIS_STATE_FULL_CALIBRATION_SEQUENCE)
            input('\nPress enter when u heared <beep> and motor cw and ccw')

            self.stop()
            self.m1.motor.config.pre_calibrated = True
            self.m1.encoder.config.pre_calibrated = True 

            self.save_cfg()
            self.reboot()
            
        log.success('ODrive configured successfully, congrats!')

    def start(self) -> None:
        self.m0.set_state(AXIS_STATE_CLOSED_LOOP_CONTROL)
        self.m1.set_state(AXIS_STATE_CLOSED_LOOP_CONTROL)

    def stop(self) -> None:
        self.m0.set_state(AXIS_STATE_IDLE)
        self.m1.set_state(AXIS_STATE_IDLE)


if __name__ == "__main__":
    odrv = ODriveAPI()
    odrv.start()
    
    vel, tmr = 1, None
    
    while True:
        if time() - tmr > 1000:
            vel *= -1
        try:
            odrv.m0.set_vel(vel)
            odrv.m1.set_vel(vel)

        except KeyboardInterrupt:
            break;
    odrv.stop()
