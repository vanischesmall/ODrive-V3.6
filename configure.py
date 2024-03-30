import odrive
from odrive.enums import *

from dataclasses import dataclass 


class Encoder:
    def __init__(self,
                 mode: int = ENCODER_MODE_HALL, 
                 bandwidth: int = 100,
                 cpr: int = 90):
        self.MODE = mode 
        self.BANDWIDTH = bandwidth
        self.CPR = cpr

class Motor:
    def __init__(self, 
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
                 ):
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
        self.VEL_INTEGRATOR_GAIN = vel_integrator_gain * self.TORQUE_CONSTANT * encoder.CPR


def configure(odrive, axis_num: int, motor: Motor) -> bool:
    ...

