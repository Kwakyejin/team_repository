import cv2
import numpy as np

a = input().split()
x_index, y_index = [], []
x_,y_ = [], []
src = cv2.imread(a[0])
# src = cv2.imread("5.png")
#src = cv2.resize(src, dsize = (480, 480))
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV())
lower_green = np.array([40, 70, 70])
upper_green = np.array([80, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)
dst = cv2.cornerHarris(mask, 9, 31, 0.08)
dst = cv2.dilate(dst,None)
src[dst>0.01*dst.max()]=[0,0,255]
coord = np.where(dst>0.01*dst.max())
y = coord[0]; x = coord[1]
for i, j in zip(set(x), set(y)):
    x_index.append(list(x).count(i))
    y_index.append(list(y).count(j))
#print(x_index)
l = 1
while len(x_) < 2:
    cnt = 0
    if len(x_) == 0:
        x_.append(list(set(x))[x_index.index(sorted(x_index)[-1])])
        x_index[x_index.index(sorted(x_index)[-1])] = -1
    for k in x_:
        if abs(k - list(set(x))[x_index.index(sorted(x_index)[-1])]) < 8:
            x_index[x_index.index(sorted(x_index)[-1])] = -1
            break
        cnt += 1
    if cnt == len(x_):
        x_.append(list(set(x))[x_index.index(sorted(x_index)[-1])])
        x_index[x_index.index(sorted(x_index)[-1])] = -1

while len(y_) < 2:
    cnt = 0
    if len(y_) == 0:
        y_.append(list(set(y))[y_index.index(sorted(y_index)[-1])])
        y_index[y_index.index(sorted(y_index)[-1])] = -1
    for k in y_:
        if abs(k - list(set(y))[y_index.index(sorted(y_index)[-1])]) < 8:
            y_index[y_index.index(sorted(y_index)[-1])] = -1
            break
        cnt += 1
    if cnt == len(y_):
        y_.append(list(set(y))[y_index.index(sorted(y_index)[-1])])
        y_index[y_index.index(sorted(y_index)[-1])] = -1
if ((sum(x_)/2-a[1])**2 + (sum(y_)/2-a[2])**2)<10:
    print('True')
else:
    print('False')
# print(x_, y_)
# for i in zip(x_,y_):
    # cv2.circle(src, i, 5,(0,255,255), -1)
# cv2.circle(src, (int(sum(x_)/2),int(sum(y_)/2)), 5, (0,255,255), -1)
# cv2.imshow('asdasdasd',src)
# cv2.imshow('sadad',mask)
cv2.waitKey(0)
