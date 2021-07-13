from new_drone import *
import cv2
import numpy as np
from e_drone.drone import *
from e_drone.protocol import *
import time

try:
    drone = initialize()
    drone.sendTakeOff()
    time.sleep(3)
    drone.sendControlWhile(0, 0, 0, 0, 1000)
    print('start')
    match_center(drone)
    print('finish1')
    time.sleep(5)
    match_center(drone)
    print('finish2')
    time.sleep(5)
    match_center(drone)
    print('finish3')
    drone.close()
except KeyboardInterrupt:
    drone.sendLanding()
    drone.close()
    print('stop')
except Exception as e:
    drone.sendLanding()
    drone.close()
    print(e)

