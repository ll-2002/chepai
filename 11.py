import cv2 as cv

# ·��ΪӢ��
image = cv.imread('hh.JPG')

# ��ͼƬתΪ�Ҷ�ͼ
gray_image = cv.cvtColor(image, code=cv.COLOR_BGR2GRAY)

# ��ʾͼƬ
cv.imshow('image', gray_image)
# �ȴ��������룬��λ�Ǻ��룬0��ʾ���޵ȴ�
cv.waitKey(0)
# ��Ϊ���յ��õ���C++��������ʹ����Ҫ�ͷ��ڴ�
cv.destroyAllWindows()