# # import cv2
# # import numpy as np
# # filename = '5.jpg'
# # img = cv2.imread(filename)
# # img = cv2.resize(img,dsize = (128,128))
# # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# # gray = np.float32(img)
# # dst = cv2.cornerHarris(gray,2,3,0.04)
# # img[dst>0.01*dst.max()]=[0,0,255]
# # cv2.imshow('dst',img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()

# import cv2
# import numpy as np
# a = input().split()
# filename = a[0]
# img = cv2.imread(filename)
# img = cv2.resize(img,dsize = (1080,780))
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray',gray)
# # find Harris corners
# gray = np.float32(gray)
# dst = cv2.cornerHarris(gray,2,3,0.04)
# dst = cv2.dilate(dst,None)
# ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
# dst = np.uint8(dst)
# # find centroids
# ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
# # define the criteria to stop and refine the corners
# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
# corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
# # Now draw them
# res = np.hstack((centroids,corners))
# res = np.int0(res)
# img[res[:,1],res[:,0]] = [0,0,255]
# img[res[:,3],res[:,2]] = [0,255,0]
# cv2.imshow('dst',img)
# cv2.imshow('gray',gray)
# print(res[:,1],res[:,0],res[:,3],res[:,2])
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#---------------------------------------------------------------------------------------------------------------
#2021/06/28
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
