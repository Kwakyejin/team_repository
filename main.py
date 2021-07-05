from drone import *
import cv2
import numpy as np
from e_drone.drone import *
from e_drone.protocol import *
import time


drone = Drone()
drone.open()
# drone.sendTakeOff()
print('check')
time.sleep(1)
x, y = check_distance()
move_to_center(x, y)
print('finish')
time.sleep(5)
# drone.sendLanding()
# pass_obstacle()
