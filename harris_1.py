import cv2

src = cv2.imread("multiobs.jpg")
src = cv2.resize(src, dsize = (480, 480))
dst = src.copy()

gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 5, blockSize=3, useHarrisDetector=True, k=0.03)


for i in corners:

    cv2.circle(dst, (int(i[0,0]),int(i[0,1])), 2, (0, 0, 255), 1)
    # print((int(i[0,0]),int(i[0,1])))
cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
