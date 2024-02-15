from rozenODriver import rozenODriver
from odrive.enums import *

from time import sleep


odrive = rozenODriver()
if __name__ == "__main__":
    odrive.set_state(AXIS_STATE_CLOSED_LOOP_CONTROL)
    
    while True:
        try:
            odrive.set_velocity(2, 0)
          

        except KeyboardInterrupt:
            odrive.stop()
            break
        
