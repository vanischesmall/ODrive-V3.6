# ODrive V3.6 Configuration for VisionRide motors

## Full Calibration Sequence

```Shell
odrv0.erase_configuration()
```

```Shell
odrv0.axis0.motor.config.pole_pairs = 15;
odrv0.axis0.motor.config.resistance_calib_max_voltage = 4;
odrv0.axis0.motor.config.requested_current_range = 25;
odrv0.axis0.motor.config.current_control_bandwidth = 100;
odrv0.axis0.motor.config.torque_constant = 8.27 / 16;
odrv0.axis0.motor.config.calibration_current = 5;
odrv0.axis0.encoder.config.mode = ENCODER_MODE_HALL;
odrv0.axis0.encoder.config.bandwidth = 100;
odrv0.axis0.encoder.config.cpr = 90;
odrv0.axis0.controller.config.pos_gain = 1;
odrv0.axis0.controller.config.vel_gain = 0.02 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr;
odrv0.axis0.controller.config.vel_integrator_gain = 0.1 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr;
odrv0.axis0.controller.config.vel_limit = 4;

odrv0.axis1.motor.config.pole_pairs = 15;
odrv0.axis1.motor.config.resistance_calib_max_voltage = 4;
odrv0.axis1.motor.config.requested_current_range = 25;
odrv0.axis1.motor.config.current_control_bandwidth = 100;
odrv0.axis1.motor.config.torque_constant = 8.27 / 16;
odrv0.axis1.motor.config.calibration_current = 5;
odrv0.axis1.encoder.config.mode = ENCODER_MODE_HALL;
odrv0.axis1.encoder.config.bandwidth = 100;
odrv0.axis1.encoder.config.cpr = 90;
odrv0.axis1.controller.config.pos_gain = 1;
odrv0.axis1.controller.config.vel_gain = 0.02 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr;
odrv0.axis1.controller.config.vel_integrator_gain = 0.1 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr;
odrv0.axis1.controller.config.vel_limit = 4;

odrv0.save_configuration();
odrv0.reboot();
```

**_Be sure M0 if free to move_**

```Shell
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE;
```

**_Be sure M1 if free to move_**

```Shell
odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE;
```

```Shell
odrv0.axis0.requested_state = AXIS_STATE_IDLE;
odrv0.axis0.encoder.config.pre_calibrated = True;
odrv0.axis0.motor.config.pre_calibrated = True;

odrv0.axis1.requested_state = AXIS_STATE_IDLE;
odrv0.axis1.encoder.config.pre_calibrated = True;
odrv0.axis1.motor.config.pre_calibrated = True;

odrv0.save_configuration();
odrv0.reboot();
```

## Erase config

```Shell
odrv0.erase_configuration()
```

## Axis0

```Shell
odrv0.axis0.motor.config.pole_pairs = 15;
odrv0.axis0.motor.config.resistance_calib_max_voltage = 4;
odrv0.axis0.motor.config.requested_current_range = 25;
odrv0.axis0.motor.config.current_control_bandwidth = 100;
odrv0.axis0.motor.config.torque_constant = 8.27 / 16;
odrv0.axis0.motor.config.calibration_current = 5;
odrv0.axis0.encoder.config.mode = ENCODER_MODE_HALL;
odrv0.axis0.encoder.config.bandwidth = 100;
odrv0.axis0.encoder.config.cpr = 90;
odrv0.axis0.controller.config.pos_gain = 1;
odrv0.axis0.controller.config.vel_gain = 0.02 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr;
odrv0.axis0.controller.config.vel_integrator_gain = 0.1 * odrv0.axis0.motor.config.torque_constant * odrv0.axis0.encoder.config.cpr;
odrv0.axis0.controller.config.vel_limit = 4;
odrv0.save_configuration();
odrv0.reboot();
```

```Shell
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE;
```

```Shell
odrv0.axis0.requested_state = AXIS_STATE_IDLE;
odrv0.axis0.encoder.config.pre_calibrated = True;
odrv0.axis0.motor.config.pre_calibrated = True;
odrv0.save_configuration();
odrv0.reboot();
```

## Axis 1

```Shell
odrv0.axis1.motor.config.pole_pairs = 15;
odrv0.axis1.motor.config.resistance_calib_max_voltage = 4;
odrv0.axis1.motor.config.requested_current_range = 25;
odrv0.axis1.motor.config.current_control_bandwidth = 100;
odrv0.axis1.motor.config.torque_constant = 8.27 / 16;
odrv0.axis1.motor.config.calibration_current = 5;
odrv0.axis1.encoder.config.mode = ENCODER_MODE_HALL;
odrv0.axis1.encoder.config.bandwidth = 100;
odrv0.axis1.encoder.config.cpr = 90;
odrv0.axis1.controller.config.pos_gain = 1;
odrv0.axis1.controller.config.vel_gain = 0.02 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr;
odrv0.axis1.controller.config.vel_integrator_gain = 0.1 * odrv0.axis1.motor.config.torque_constant * odrv0.axis1.encoder.config.cpr;
odrv0.save_configuration();
odrv0.reboot();
```

```Shell
odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
```

```Shell
odrv0.axis1.requested_state = AXIS_STATE_IDLE;
odrv0.axis1.encoder.config.pre_calibrated = True;
odrv0.axis1.motor.config.pre_calibrated = True;
odrv0.save_configuration();
odrv0.reboot();
```
