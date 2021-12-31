import cv2 as cv

# 路径为英文
image = cv.imread('hh.JPG')

# 将图片转为灰度图
gray_image = cv.cvtColor(image, code=cv.COLOR_BGR2GRAY)

# 显示图片
cv.imshow('image', gray_image)
# 等待键盘输入，单位是毫秒，0表示无限等待
cv.waitKey(0)
# 因为最终调用的是C++对象，所以使用完要释放内存
cv.destroyAllWindows()