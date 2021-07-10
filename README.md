# '2021(이공이일)' Drone B리그 README

## 참가자
부산대학교 의생명융합공학부 2학년 곽예진

부산대학교 의생명융합공학부 2학년 강준희

부산대학교 의생명융합공학부 1학년 안수범

## 대회 진행 전략


## 알고리즘 설명
*main idea -> 중심을 찾고 중심을 찾은 이후에는 장애물을 통과한다.*

hovering 후 드론 내장된 카메라로 하나의 이미지를 찍는다. 이때 중심을 (120, 150*) 으로 둔다. *완전한 중심은 (120,120)이지만 카메라가 드론의 아래에 달려있기 때문이다.*

그리고 난 후 find_centroid로 찾은 중점을 중심 방향으로 이동할 수 있게 드론을 움직여준다.

처음 찍힌 원과 중심, 중심 방향으로 이동한 원과 중심의 비율 통해서 중심 방향으로 이동한 원에서 얼만큼 x,y 축으로 이동하면 중심에 도달할지 알 수 있다. -> check_distance

중심에 도달한 이후에는 쭉 직진을 한다.

find_redpoint와 find_purplepoint로 빨간점, 보라점을 찾고 찾은 이후에는 pass_obstacle로 보라점을 찾았을 시에는 착지, 빨간점을 찾았을 시에는 90도 좌회전을 한다. 

## 소스 코드 설명
### requirement
```py
import cv2
import numpy as np
from e_drone.drone import *
from e_drone.protocol import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
```
### drone.py
드론에 대한 함수를 정의한 파이썬 
1. initialize

드론 객체를 생성하고 드론 조작을 시작하기 위한 함수
```py
drone = Drone()
drone.open()
return drone
```

2. capture_img

라즈베리파이 카메라 모듈을 카메라로 보이는 장면을 캡쳐해준다. resolution은 (240,240), frame rate는 32이고 찍으면 뒤집혀 찍히기 때문에 rotation을 180으로 설정해준다.
```py
camera = PiCamera()
img = 'img.jpg'
camera.resolution = (240, 240)  # 160, 128
camera.framerate = 32
camera.rotation = 180
camera.capture(img)
camera.close()
return img  # capture img path
```

3. find_centroid**

<이미지 처리 과정>
우선 이미지를 blur처리를 해준다. ->cv2.GaussianBlur

lower_blue, upper_blue라는 array를 만들어 주고 카메라로 캡쳐한 화면에서 이 범위에 있는 부분을 mask처리한다. -> cv2. 

<드론 명령 결정 과정>
계층 파악(->)을 통해 원이 잘리게 화면에 직힌다면 드론이 후진을 하도록 하였고 
그렇지 않다면

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(len(hierarchy[0]))

    if len(hierarchy[0]) <= 1 or hierarchy == None:
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

4. check_distance**

find_centroid를 통해 무게 중심(cx, cy)을 찾고 무게 중심 값이 처음 설정한 값보다 클 시에는 0.15에 (-)를 달아주었다.
*중심에 가까워질려면 음의 값이어야하기 때문이다, 0.15는*

그 값을 mx, my로 지정하고 그만큼 드론을 이동시켜준다.
   
다시 find_centroid를 통해 무게 중심(cx2, cy2)을 찾고 
0.15 * (cx2 - 120) / (cx - cx2), 0.15 * (cy2 - 140) / (cy - cy2) 의 값을 반환해준다.
    

    # change_f = abs(cx - cx2)# cx_2
    # m_per_f = 0.2/change_f
    # x = 120 - cx2 # x > 0 go right x < 0 go left
    # y = 120 - cy2 # y > 0 go up y < 0 go down
    print(cx, cy, cx2, cy2)  # ,m_per_f)
    return 0.15 * (cx2 - 120) / (cx - cx2), 0.15 * (cy2 - 140) / (cy - cy2)  # x*m_per_f, y*m_per_f

5. check_center

find_centroid 함수의 <이미지 처리 과정>를 똑같이 거친다.

contour를 이용해서 안의 위치한 원의 무게중심을 파악한다.
```py
cnt = contours[1]
M = cv2.moments(cnt)
cx = int(M['m10'] / (M['m00'] + 0.000000000000001))
cy = int(M['m01'] / (M['m00'] + 0.000000000000001))
```
cx와 cy의 값이 처음 중심이라 잡은 (120, 150*)와 10 이하의 차이가 난다면 True, 아니라면 False를 반환한다.
        
6. move_to_center**

drone.sendControlPosition(0, x, y, 1, 0, 0)  # +y = left -y = right
만약 check_center가 True로 반환되면 pass_obstacle을 하고 아닐시에는 check_distance로 거리를 다시 측정한 다음 move_to_center를 다시 해준다.

7. find_redpoint

<이미지 처리 과정>
우선 이미지를 blur처리를 해준다. ->cv2.GaussianBlur

lower_red, upper_red라는 array를 만들어 주고 카메라로 캡쳐한 화면에서 이 범위에 있는 부분을 mask처리한다. -> cv2. 

point_red = np.nonzero(mask)
num_point_red = np.size(point_red)
#cv2.imshow('img',img)
cv2.imshow('mask',mask)
cv2.waitKey(0)
return num_point_red

8. find_purplepoint

<이미지 처리 과정>
우선 이미지를 blur처리를 해준다. ->cv2.GaussianBlur

lower_purple, upper_purple라는 array를 만들어 주고 카메라로 캡쳐한 화면에서 이 범위에 있는 부분을 mask처리한다. -> cv2. 
4*4*
    point_purple = np.nonzero(mask)
    num_point_purple = np.size(point_purple)
    return num_point_purple

9. pass_obstacle**
find_purplepoint의 값이 100보다 작을시에는 드론을 착륙시키고 드론 객체를 종료시킨다.

find_redpoint의 값이 110보다 작을 시에는 드론을 x축으로 0.5 이동시킨 다음 pass_obstacle를 다시 실행시본다.

find_redpoint의 값이 110보다 클 시에는 드론을 90도로 좌회전을 시켜준다.

### main.py
드론이 이동 할 수 있도록 drone.py에 만든 함수를 나열한 파일

drone이라는 객체를 생성한 다음 drone을 이륙하도록 하게 함 -> drone.sendTakeOff()

차례로 check_distance(drone), move_to_center(drone, x, y)이라는 함수를 실행시켜준다.

3차례 반복 뒤 드론이 착륙을 하게 하도록 함. -> drone.sendLanding()
