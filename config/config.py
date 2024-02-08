import argparse, sys, time 

import odrive


class Parser:
    def __init__(self) -> object:
        self.parser = argparse.ArgumentParser(description = "ODrive V3.6 Motor Configuration")

        self.parser.add_argument("--axis", type = int, choices = [0, 1, 2], required = True,
                                 help = "Enter number of configurable axis")
        self.parser.add_argument("--erase_config", action = "store_true",
                                 help = "Enter if config should be erased")
    
    def get_arguments() -> None:
        self.arguments = parser.parse_args()


class Controller:
    def __init__(self, 
                 position_gain: float = 1.0,
                 velocity_gain: float = 0.02,
                 velocity_integrator_gain: float = 0.1,
                 velocity_limit: float = 3.0) -> object:
        self.position_gain = position_gain
        self.velocity_gain = velocity_gain
        self.velocity_integrator_gain = velocity_integrator_gain
        self.velocity_limit = velocity_limit


class Motor:
    def __init__(self, kv: int, 
                 pole_pairs: int,
                 resistance_calib_max_voltage: int,
                 requested_current_range: int,
                 current_control_bandwidth: int,
                 calibration_current: int) -> object:
        self.kv = kv
        self.pole_pairs = pole_pairs
        self.resistance_calib_max_voltage = resistance_calib_max_voltage
        self.requested_current_range = requested_current_range
        self.current_control_bandwidth = current_control_bandwidth
        self.torque_constant = 8.27 / self.kv
        self.calibration_current = calibration_current


class Encoder:
    def __init__(self, mode: odrive.enums, cpr: int, bandwidth: int) -> object:
        self.mode = mode
        self.cpr = cpr
        self.bandwidth = bandwidth
        

class ODrive:
    def __init__(self) -> object:
        self.odrv = odrive.find_any()

    def configure(self, axis_number: int, motor: Motor, encoder: Encoder, controller: Controller) -> None:
        self.axis = getattr(self.odrv, f'axis{axis_number}')
        
        print(f'Starting configure axis{axis_number}!')

        self.axis.motor.config.pole_pairs = motor.pole_pairs
        self.axis.motor.config.resistance_calib_max_voltage = motor.resistance_calib_max_voltage
        self.axis.motor.config.requested_current_range = motor.requested_current_range
        self.axis.motor.config.current_control_bandwidth = motor.current_control_bandwidth
        self.axis.motor.config.torque_constant = motor.torque_constant
        self.axis.motor.config.calibration_current = motor.calibration_current

        self.axis.encoder.config.bandwidth = encoder.bandwidth
        self.axis.encoder.config.mode = encoder.mode
        self.axis.encoder.config.cpr = encoder.cpr

        self.axis.controller.config.pos_gain = controller.position_gain
        self.axis.controller.config.vel_gain = controller.velocity_gain * motor.torque_constant * encoder.cpr
        self.axis.controller.config.vel_integrator_gain = controller.velocity_integrator_gain * motor.torque_constant * encoder.cpr
        self.axis.controller.config.vel_limit = controller.velocity_limit

        print("Configuration done! Saving...")
        odrv.axis.requested_state = odrive.enums.AXIS_STATE_IDLE
        is_saved = self.odrv.save_configuration()
        if is_saved:
            print("Configuration saved successfully! Reboot required, rebooting...")
        else:
            print("Error while saving")
        self.odrv.reboot()

    def erase_configuration(self) -> None:
        print("Erasing pre-existing configuration...")
        
        try:
            self.odrv.erase_configuration()
            print("Configuration erased!")
        except:
            print("Oops!.. Error while erasing")
        
        self.odrv.find_any()


if __name__ == "__main__": 
    m0 = Motor(
            kv = 16,
            pole_pairs = 15,
            resistance_calib_max_voltage = 4,
            requested_current_range = 25,
            current_control_bandwidth = 100,
            calibration_current = 5
            )
    e0 = Encoder(
            mode = odrive.enums.ENCODER_MODE_HALL,
            cpr = 90,
            bandwidth = 100
            )

    m1 = Motor(
            kv = 16,
            pole_pairs = 15,
            resistance_calib_max_voltage = 4,
            requested_current_range = 25,
            current_control_bandwidth = 100,
            calibration_current = 5
            )
    e1 = Encoder(
            mode = odrive.enums.ENCODER_MODE_HALL,
            cpr = 90,
            bandwidth = 100
            )

    controller = Controller(
            position_gain = 1,
            velocity_gain = 0.02,
            velocity_integrator_gain = 0.1,
            velocity_limit = 3.0
            )
    
    odrv = ODrive()
    odrv.configure(axis_number = 0, motor = m0, encoder = e0, controller = controller)
    odrv.configure(axis_number = 1, motor = m1, encoder = e1, controller = controller)
