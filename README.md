# '2021(이공이일)' Drone B리그 README


## 참가자
부산대학교 의생명융합공학부 2학년 곽예진

부산대학교 의생명융합공학부 2학년 강준희

부산대학교 의생명융합공학부 1학년 


## 대회 진행 전략

B리그 분들의 알고리즘은 똑같이 중심을 찾고 중심 쪽으로 드론을 위치 시간 다음 장애물을 통과한다는 것일 것이다. 

그렇기에 코드의 Runtime을 줄이거나 원하는 값을 빨리 얻도록 하는 조정값을 찾도록 하는 것이 2021(이공이일) 팀의 전략이다.


## 알고리즘 설명
*main idea -> 중심을 찾고 중심 쪽으로 드론을 위치 시간 다음 장애물을 통과한다.*

- hovering 후 드론 내장된 카메라로 하나의 이미지를 찍는다. 이때 중심을 (120, 140*) 으로 둔다. 

*완전한 중심은 (120,120)이지만 카메라가 드론의 아래에 달려있기 때문이다.*

- 그리고 난 후 find_centroid로 찾은 중점을 중심 방향으로 이동할 수 있게 드론을 움직여준다.

- 처음 찍힌 원과 중심, 중심 방향으로 이동한 원과 중심의 비율 통해서 중심 방향으로 이동한 원에서 얼만큼 x,y 축으로 이동하면 중심에 도달할지 알 수 있다. -> check_distance

- 중심에 도달한 이후에는 쭉 직진을 한다. -> pass_obstacle

- find_redpoint와 find_purplepoint로 빨간점, 보라점을 찾고 찾은 이후에는 pass_obstacle로 보라점을 찾았을 시에는 착지, 빨간점을 찾았을 시에는 90도 좌회전을 한다. -> pass_obstacle


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


**1. initialize**

드론 객체를 생성하고 드론 조작을 시작하기 위한 함수
```py
drone = Drone()
drone.open()
return drone
```


**2. capture_img**

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


**3. find_centroid**

<이미지 처리 과정>

- 우선 이미지를 blur처리를 해준다. -> cv2.GaussianBlur

- 이미지의 BGR로 HSV값으로 바꿔준다. -> cv2.COLOR_BGR2HSV

- lower_blue, upper_blue라는 array를 만들어 주고 카메라로 캡쳐한 화면에서 이 범위에 있는 부분을 mask처리한다. -> cv2.inRange

<원 중심  과정>

- 계층 파악을 통해 원이 잘리게 화면에 직힌다면 드론이 후진을 하도록 하였고 
```py
if len(hierarchy[0]) <= 1 or hierarchy == None:
```
- 그렇지 않다면 contour를 이용해서 안의 위치한 원의 무게중심을 파악한다.
- zerodivision 에러를 막기 위해 분모에 아주 작은 실수를 더해준다.
```py
cnt = contours[1]
...
M = cv2.moments(cnt)
cx = int(M['m10'] / (M['m00'] + 0.000000000000001))
cy = int(M['m01'] / (M['m00'] + 0.000000000000001))
...
return cx, cy
```


**4. check_distance**

- find_centroid를 통해 무게 중심(cx, cy)을 찾고 무게 중심 값이 처음 설정한 값보다 클 시에는 0.15에 (-)를 달아주었다.

*중심에 가까워질려면 음의 값이어야하기 때문이다, 0.15는 움직이는 거리이다.*

- 그 값을 mx, my로 지정하고 그만큼 드론을 이동시켜준다.
   
- 다시 find_centroid를 통해 무게 중심(cx2, cy2)을 찾고 
0.15 * (cx2 - 120) / (cx - cx2), 0.15 * (cy2 - 140) / (cy - cy2) 의 값을 반환해준다.
    
    
**5. check_center**

- find_centroid 함수의 <이미지 처리 과정>를 똑같이 거친다.

- contour를 이용해서 안의 위치한 원의 무게중심을 파악한다.
```py
cnt = contours[1]
M = cv2.moments(cnt)
cx = int(M['m10'] / (M['m00'] + 0.000000000000001))
cy = int(M['m01'] / (M['m00'] + 0.000000000000001))
```
- cx와 cy의 값이 처음 중심이라 잡은 (120, 140*)와 10 이하의 차이가 난다면 True, 아니라면 False를 반환한다.
 
 
**6. move_to_center**

- check_distance의 return 값을 x, y로 받고 drone을 x, y 만큼 움직인다. 
```py
drone.sendControlPosition(0, x, y, 1, 0, 0) 
```

- check_center가 True로 반환되면 pass_obstacle을 하고 아닐시에는 check_distance로 거리를 다시 측정한 다음 move_to_center를 다시 해준다.


**7. find_redpoint**

<이미지 처리 과정>

- 우선 이미지를 blur처리를 해준다. ->cv2.GaussianBlur

- lower_red, upper_red라는 array를 만들어 주고 카메라로 캡쳐한 화면에서 이 범위에 있는 부분을 mask처리한다. -> cv2.inRange 

- mask 처리된 것에서 np.nonzero의 갯수를 알아내서 return 해준다.
```py
point_red = np.nonzero(mask)
num_point_red = np.size(point_red)
return num_point_red
```



**8. find_purplepoint**

<이미지 처리 과정>

- 우선 이미지를 blur처리를 해준다. ->cv2.GaussianBlur

- lower_purple, upper_purple라는 array를 만들어 주고 카메라로 캡쳐한 화면에서 이 범위에 있는 부분을 mask처리한다. -> cv2.inRange

- mask 처리된 것에서 np.nonzero의 갯수를 알아내서 return 해준다.
```py
point_purple = np.nonzero(mask)
num_point_purple = np.size(point_purple)
return num_point_purple
```


**9. pass_obstacle**

- find_purplepoint의 값이 100보다 작을시에는 드론을 착륙시키고 드론 객체를 종료시킨다.

- find_redpoint의 값이 110보다 작을 시에는 드론을 x축으로 0.5 이동시킨 다음 pass_obstacle를 다시 실행시켜본다.

- find_redpoint의 값이 110보다 클 시에는 드론을 90도로 좌회전을 시켜준다.


### main.py
드론이 이동 할 수 있도록 drone.py에 만든 함수를 나열한 파일

- drone이라는 객체를 생성한 다음 drone을 이륙하도록 하게 함 -> drone.sendTakeoff()

- 차례로 check_distance(drone), move_to_center(drone, x, y)이라는 함수를 실행시켜준다.

- 3차례 반복 뒤 드론이 착륙을 하게 하도록 함. -> drone.sendLanding()
