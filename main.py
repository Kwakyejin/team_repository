from drone import *
import cv2
import numpy as np

img = capture_img()
x,y = check_distance(img)
move_to_center(x,y)
# pass_obstacle()
