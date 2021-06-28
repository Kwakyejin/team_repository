import cv2
import numpy as np

x, y = [], []
x_, y_ = [], []
x_index, y_index = [], []
a = input().split()
lower_green = np.array([40, 70, 70])
upper_green = np.array([80, 255, 255])
img = cv2.imread(a[0])
img = cv2.GaussianBlur(img, (9,9),3)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_green, upper_green)

c, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for j in c[1].tolist():
    y_.append(j[0][1])
    x_.append(j[0][0])
for i, j in zip(set(x_),set(y_)):
    x_index.append(x_.count(i))
    y_index.append(y_.count(j))

while len(x) < 2:
    cnt = 0
    if len(x) == 0:
        x.append(list(set(x_))[x_index.index(sorted(x_index)[-1])])
        x_index[x_index.index(sorted(x_index)[-1])] = -1
    for k in x:
        if abs(k - list(set(x_))[x_index.index(sorted(x_index)[-1])]) < 90:
            x_index[x_index.index(sorted(x_index)[-1])] = -1
            break
        cnt += 1
    if cnt == len(x):
        x.append(list(set(x_))[x_index.index(sorted(x_index)[-1])])
        x_index[x_index.index(sorted(x_index)[-1])] = -1

while len(y) < 2:
    cnt = 0
    if len(y) == 0:
        y.append(list(set(y_))[y_index.index(sorted(y_index)[-1])])
        y_index[y_index.index(sorted(y_index)[-1])] = -1
    for k in y:
        if abs(k - list(set(y_))[y_index.index(sorted(y_index)[-1])]) < 20:
            y_index[y_index.index(sorted(y_index)[-1])] = -1
            break
        cnt += 1
    if cnt == len(y):
        y.append(list(set(y_))[y_index.index(sorted(y_index)[-1])])
        y_index[y_index.index(sorted(y_index)[-1])] = -1

if (((max(x_)+min(x_))/2-int(a[1]))**2 + ((max(y_)+min(y_))/2-int(a[2]))**2)<50:
    print('True')
else:
    print('False')
#for i,j in zip(x,y):
    #cv2.circle(img,(i, j),2,(0,255,255), -1)
    #print(i, j)
#print(int(sum(x)/2), int(sum(y)/2))
#print(int((max(x_)+min(x_))/2), int((max(y_)+min(y_))/2))
