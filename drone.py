import cv2
import numpy as np
from e_drone.drone import *
from e_drone.protocol import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


# sendControlPosition(self, positionX, positionY, positionZ, velocity, heading, rotationalVelocity):

def initialize():
    drone = Drone()
    drone.open()
    return drone


def capture_img():
    camera = PiCamera()
    img = 'img.jpg'
    camera.resolution = (240, 240)  # 160, 128
    camera.framerate = 32
    camera.rotation = 180
    camera.capture(img)
    camera.close()
    return img  # capture img path


def find_centroid(drone):  # centroid = 240x240 in (480x480) // need to recheck
    lower_blue = np.array([100, 80, 80])
    upper_blue = np.array([110, 255, 255])

    img = cv2.imread(capture_img())
    img = cv2.GaussianBlur(img, (9, 9), 3)

    # img = cv2.resize(img, dsize=(240,240))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)

    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(len(hierarchy[0]))

    # img = cv2.drawContours(img, contours, -1, (255,255,0), 3)
    if len(hierarchy[0]) <= 1 or None:
        print("go back")
        cv2.imshow('img', img)
        cv2.imshow('mask', mask)
        cv2.waitKey(0)

        drone.sendControlPosition(-0.5, 0, 0, 1, 0, 0)
        time.sleep(7)
        return find_centroid(drone)

    else:
        cnt = contours[1]
        img = cv2.drawContours(img, contours, 1, (255, 255, 0), 3)
        M = cv2.moments(cnt)
        cx = int(M['m10'] / (M['m00'] + 0.000000000000001))
        cy = int(M['m01'] / (M['m00'] + 0.000000000000001))
        cv2.circle(img, (cx, cy), 4, (255, 255, 0), -1)
        print(cx, cy)
        cv2.imshow('img', img)
        cv2.imshow('mask', mask)
        cv2.waitKey(0)
        return cx, cy


def check_distance(drone):
    cx, cy = find_centroid(drone)
    mx = -0.15 if cx >= 120 else 0.15
    my = -0.15 if cy >= 140 else 0.15

    print('first ok')
    time.sleep(5)
    print('move')
    drone.sendControlPosition(0, mx, my, 1, 0, 0)
    time.sleep(5)
    cx2, cy2 = find_centroid(drone)
    print('second ok')
    # change_f = abs(cx - cx2)# cx_2
    # m_per_f = 0.2/change_f
    # x = 120 - cx2 # x > 0 go right x < 0 go left
    # y = 120 - cy2 # y > 0 go up y < 0 go down
    print(cx, cy, cx2, cy2)  # ,m_per_f)
    return 0.15 * (cx2 - 120) / (cx - cx2), 0.15 * (cy2 - 140) / (cy - cy2)  # x*m_per_f, y*m_per_f

def check_center():
    lower_green = np.array([50, 128, 50])
    upper_green = np.array([80, 255, 255])

    img = cv2.imread(capture_img())
    img = cv2.GaussianBlur(img, (9, 9), 3)

    # img = cv2.resize(img, dsize=(240,240))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[1]
    M = cv2.moments(cnt)
    cx = int(M['m10'] / (M['m00'] + 0.000000000000001))
    cy = int(M['m01'] / (M['m00'] + 0.000000000000001))
    print('check_center : ',cx, cy)
    if abs(cx-120) < 10 and abs(cy-140) < 10:
        return True
    else:
        return False

def move_to_center(drone, x, y):
    print('move to center')
    drone.sendControlPosition(0, x, y, 1, 0, 0)  # +y = left -y = right
    time.sleep(5)
    if check_center():
        pass_obstacle(drone)
    else:
        x1, y1 = check_distance(drone)
        move_to_center(drone, x1, y1)
    #pass_obstacle(drone)


def find_redpoint():
    img = cv2.imread(capture_img())
    upper_red = np.array([15,255,255])
    lower_red = np.array([0,50,80])
    img = cv2.GaussianBlur(img, (9, 9), 2.5)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    point_red = np.nonzero(mask)
    num_point_red = np.size(point_red)
    #cv2.imshow('img',img)
    cv2.imshow('mask',mask)
    cv2.waitKey(0)
    return num_point_red

def find_purplepoint():
    img = cv2.imread(capture_img())
    upper_purple = np.array([112,48,160])
    lower_purple = np.array([90,40,100])
    img = cv2.GaussianBlur(img, (9, 9), 2.5)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    point_purple = np.nonzero(mask)
    num_point_purple = np.size(point_purple)
    return num_point_purple


def pass_obstacle(drone):
    #if find_purplepoint() > 100:
        #print('detect purple point')
        #drone.sendLanding()
        #drone.close()
        #return 0
        
    if find_redpoint() < 110:
    drone.sendControlPosition(0.5, 0, 0, 1, 0, 0)
    print('not find red(purple) point')
    time.sleep(7)
    pass_obstacle(drone)

    else:
        drone.sendControlPosition(0, 0, 0, 0, 90, 18)
        print('find red point')

        time.sleep(5)
        return 0

    



