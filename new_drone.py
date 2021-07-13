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
    while True:
        img = cv2.imread(capture_img())
        img = cv2.GaussianBlur(img, (9, 9), 3)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        print(len(hierarchy[0]))

        if len(hierarchy[0]) <= 1:
            print("go back")
            cv2.imshow('mask', mask)
            cv2.waitKey(0)
            drone.sendControlPosition(-0.5, 0, 0, 1, 0, 0)
            time.sleep(5)

        else:
            cnt = contours[0]
            img = cv2.drawContours(img, contours, 0, (255, 255, 0), 3)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / (M['m00'] + 0.000000000000001))
            cy = int(M['m01'] / (M['m00'] + 0.000000000000001))
            cv2.circle(img, (cx, cy), 4, (255, 255, 0), -1)
            print(cx, cy)
            cv2.imshow('mask', mask)
            cv2.waitKey(0)
            return cx, cy

def match_center(drone):
    while not check_center(drone):
        x, y = find_centroid(drone)
        print(x, y)
        if x < 120:
            drone.sendControlPosition(0, -0.2, 0, 1, 0, 0)
        else:
            drone.sendControlPosition(0, 0.2, 0, 1, 0, 0)
        time.sleep(5)
        

        if y < 140:
            drone.sendControlPosition(0, 0, 0.2, 1, 0, 0)
        else:
            drone.sendControlPosition(0, 0, -0.2, 1, 0, 0)
        time.sleep(5)
    pass_obstacle(drone)

def check_center(drone):
    lower_blue = np.array([100, 80, 80])
    upper_blue = np.array([110, 255, 255])

    img = cv2.imread(capture_img())
    img = cv2.GaussianBlur(img, (9, 9), 3)

    # img = cv2.resize(img, dsize=(240,240))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]
    M = cv2.moments(cnt)
    cx = int(M['m10'] / (M['m00'] + 0.000000000000001))
    cy = int(M['m01'] / (M['m00'] + 0.000000000000001))
    print('check_center : ', cx, cy)
    if abs(cx - 120) <= 10 and abs(cy - 140) <= 10:
        return True
    else:
        return False

def find_redpoint():
    img = cv2.imread(capture_img())
    upper_red = np.array([15, 255, 255])
    lower_red = np.array([0, 50, 80])
    img = cv2.GaussianBlur(img, (9, 9), 2.5)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_red, upper_red)

    point_red = np.nonzero(mask)
    num_point_red = np.size(point_red)
    print('red : ', num_point_red)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    return num_point_red


def find_purplepoint():
    img = cv2.imread(capture_img())
    upper_purple = np.array([120, 255, 255])
    lower_purple = np.array([110, 0, 0])
    img = cv2.GaussianBlur(img, (9, 9), 2.5)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    point_purple = np.nonzero(mask)
    num_point_purple = np.size(point_purple)
    print('purple : ', num_point_purple)
    return num_point_purple


def pass_obstacle(drone):
    while True:
        if find_purplepoint() > 500:
            print('detect purple point')
            drone.sendLanding()
            drone.close()
            return 0

        if find_redpoint() < 500:
            drone.sendControlPosition(0.5, 0, 0, 1, 0, 0)
            print('not find red(purple) point')
            time.sleep(7)

        else:
            drone.sendControlPosition(0, 0, 0, 0, 90, 18)
            print('find red point')
            time.sleep(5)
            return 0
