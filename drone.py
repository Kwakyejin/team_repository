import cv2
import numpy as np
from e_drone.drone import *
from e_drone.protocol import *

#sendControlPosition(self, positionX, positionY, positionZ, velocity, heading, rotationalVelocity):

def capture_img():
    #Picam capture code
    img = 'asd'
    return img # 캡쳐 이미지 경로

def find_centroid(img): # centroid = 240x240 in (480x480) // need to recheck
    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])
    k = 0
    img = cv2.imread("img")
    # img = cv2.GaussianBlur(img, (9, 9), 3)
    img = cv2.resize(img, dsize=(480,480))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy <= 1:
        print("go back")
        # sendControlPosition(0, 0.1, 0, 0.1, 0, 0)
        find_centroid(img)
    else:
        cnt = contours[0]
        M = cv2.moments(cnt)
        cx = int(M['m10'] / (M['m00'] + 0.000001))
        cy = int(M['m01'] / (M['m00'] + 0.000001))
        for i in contours:
            for j in range(len(i)):
                if k == 0:
                    # pass
                    cv2.circle(img, (int(i[j][0][0]), int(i[j][0][1])), 4, (0, 0, 255), -1)
                else:
                    cv2.circle(img, (int(i[j][0][0]), int(i[j][0][1])), 4, (255, 255, 255), -1)
            k = 1
        cv2.circle(img, (cx, cy), 4, (255, 255, 0), -1)
        cv2.imshow('asdasd', img)
        cv2.imshow('mask', mask)
        cv2.waitKey(0)
        return cx, cy

def check_distance(img):
    cx, cy = find_centroid(img)
    sendControlPosition(0, 0.1, 0, 0.1, 0, 0)
    cx2, cy2 = find_centroid(img)
    change_f = abs(cx - cx2)# cx_2
    m_per_f = 0.1/change_f
    x = 240 - cx2 # x > 0 go right x < 0 go left
    y = 240 - cy2 # y > 0 go up y < 0 go down
    return x*m_per_f, y*m_per_f

def move_to_center(x, y):
    sendControlPosition(0, -x, y, 1, 0, 0) # +y = left -y = right

