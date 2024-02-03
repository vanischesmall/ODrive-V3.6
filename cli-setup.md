to downlaod cli tool -- `yay -S python-odrive`

to enter cli tool -- `odrivetool`

to view ODrive config -- `odrv`N`.config`

to erase config -- `odrv`N`.erase_configuration`

to set motor type -- `odrv`N`.axis`X`.motor.config.motor_type = MotorType.HIGH_CURRENT`

to set pole pairs count(1/2 magnets count) -- `odrv`N`.axis`X`.motor.config.pole_pairs = 15` for our motor 

odrv0.axis0.motor.

to check errors -- dump_errors(odrv0)



