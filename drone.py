import cv2
import numpy as np
from e_drone.drone import *
from e_drone.protocol import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

#sendControlPosition(self, positionX, positionY, positionZ, velocity, heading, $

def capture_img():
    camera = PiCamera()
    img = 'img.jpg'
    camera.resolution = (240, 240)#160, 128
    camera.framerate = 32
    camera.rotation = 180
    camera.capture(img)
    camera.close()
    return img # 캡쳐 이미지 경로

def find_centroid(): # centroid = 240x240 in (480x480) // need to recheck
    drone = Drone()
    lower_green = np.array([50, 128, 50])
    upper_green = np.array([80, 255, 255])
    # k = 0
    img = cv2.imread(capture_img())
    img = cv2.GaussianBlur(img, (9, 9), 3)
    # img = cv2.resize(img, dsize=(480,480))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    drone = Drone()
    lower_green = np.array([50, 128, 50])
    upper_green = np.array([80, 255, 255])
    # k = 0
    img = cv2.imread(capture_img())
    img = cv2.GaussianBlur(img, (9, 9), 3)
    # img = cv2.resize(img, dsize=(480,480))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    _,contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPR$
    print(contours, hierarchy)
    if len(hierarchy) <= 1:
        print("go back")
        time.sleep(5)
        # drone.sendControlPosition(0, 0.1, 0, 0.1, 0, 0)
        find_centroid()
    else:
        cnt = contours[0]
        M = cv2.moments(cnt)
        cx = int(M['m10'] / (M['m00'] + 0.000001))
        cy = int(M['m01'] / (M['m00'] + 0.000001))
        # for i in contours:
        #     for j in range(len(i)):
        #         if k == 0:
        #             # pass
        #             cv2.circle(img, (int(i[j][0][0]), int(i[j][0][1])), 4, (0$
        #         else:
        #             cv2.circle(img, (int(i[j][0][0]), int(i[j][0][1])), 4, (2$
        #     k = 1
        # cv2.circle(img, (cx, cy), 4, (255, 255, 0), -1)
        # cv2.imshow('asdasd', img)
        # cv2.imshow('mask', mask)
        # cv2.waitKey(0)
        return cx, cy

def check_distance():
    drone = Drone()
    cx, cy = find_centroid()
    print('first ok')
    #drone.sendControlPosition(0, 0.1, 0, 0.1, 0, 0)
    cx2, cy2 = find_centroid()
    print('second ok')
    change_f = abs(cx - cx2)# cx_2
    m_per_f = 0.1/change_f
    x = 120 - cx2 # x > 0 go right x < 0 go left
    y = 120 - cy2 # y > 0 go up y < 0 go down
    print(cx,cy,cx2,cy2)
    return x*m_per_f, y*m_per_f
                                            
def move_to_center(x, y):
    print('move to center')
    drone = Drone()
    #drone.sendControlPosition(0, -x, y, 1, 0, 0) # +y = left -y = right





