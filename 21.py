import cv2 as cv
image = cv.imread('hh.JPG')
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
# ��ʾͼƬ
cv.imshow('hsv', hsv)
# �ȴ���������
cv.waitKey(0)