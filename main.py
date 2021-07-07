from drone import *
import cv2
import numpy as np
from e_drone.drone import *
from e_drone.protocol import *
import time


drone = initialize()
drone.sendTakeOff()
print('check')
time.sleep(1)
x, y = check_distance(drone)
move_to_center(drone, x, y)
print('finish')
time.sleep(5)
# x, y = check_distance(drone)
# move_to_center(drone, x, y)
# x, y = check_distance(drone)
# move_to_center(drone, x, y)
drone.sendLanding()
