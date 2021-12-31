import cv2 as cv
image = cv.imread('hh.JPG')
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
# ÏÔÊ¾Í¼Æ¬
cv.imshow('hsv', hsv)
# µÈ´ı¼üÅÌÊäÈë
cv.waitKey(0)