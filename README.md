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





![image](https://user-images.githubusercontent.com/81745747/124886922-a9a18c00-e00f-11eb-9c7d-8719e831bc96.png)


## 소스 코드 설명
### requirement
```py
import numpy as np
```
### drone.py

### main.py

