import cv2
import numpy as np
import os


def stackImages(scale, imgArray):
    """
        ������ͼ��ѹ��ͬһ��������ʾ
        :param scale:float���ͣ����ͼ����ʾ�ٷֱȣ��������ű�����0.5=ͼ��ֱ�����Сһ��
        :param imgArray:Ԫ��Ƕ���б���Ҫ���е�ͼ�����
        :return:���ͼ��
    """
    rows = len(imgArray)
    cols = len(imgArray[0])

    rowsAvailable = isinstance(imgArray[0], list)

    # �ÿ�ͼƬ����
    for i in range(rows):
        tmp = cols - len(imgArray[i])
        for j in range(tmp):
            img = np.zeros(
                (imgArray[0][0].shape[0], imgArray[0][0].shape[1]), dtype='uint8')
            imgArray[i].append(img)

    # �ж�ά��
    if rows >= 2:
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]

    else:
        width = imgArray[0].shape[1]
        height = imgArray[0].shape[0]

    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


# �ָ������·��
output_dir = "./output/"
# ����·��
file_path = "./car/"
# ��ȡ���г���
cars = os.listdir(file_path)
cars.sort()

# ѭ������ÿһ�ų���
for car in cars:
    # ��ȡͼƬ
    print("���ڴ���"+file_path+car)
    src = cv2.imread(file_path+car)
    img = src.copy()

    # Ԥ����ȥ����˿��
    cv2.circle(img, (145, 20), 10, (255, 0, 0), thickness=-1)
    cv2.circle(img, (430, 20), 10, (255, 0, 0), thickness=-1)
    cv2.circle(img, (145, 170), 10, (255, 0, 0), thickness=-1)
    cv2.circle(img, (430, 170), 10, (255, 0, 0), thickness=-1)
    cv2.circle(img, (180, 90), 10, (255, 0, 0), thickness=-1)

    # ת�Ҷ�
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ��ֵ��
    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 333, 1)

    # ������
    kernel = np.ones((5, 5), int)
    morphologyEx = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    # �ұ߽�
    contours, hierarchy = cv2.findContours(
        morphologyEx, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # ���߽�
    img_1 = img.copy()
    cv2.drawContours(img_1, contours, -1, (0, 0, 0), -1)

    imgStack = stackImages(
        0.7, ([src, img, gray], [adaptive_thresh, morphologyEx, img_1]))
    cv2.imshow("imgStack", imgStack)
    cv2.waitKey(0)

    # ת�Ҷ�Ϊ�˷����и�
    gray_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)

    # ÿһ�еİ�ɫ����
    white = []
    # ÿһ�еĺ�ɫ����
    black = []
    # ����߶�ȡ����ͼƬ��
    height = gray_1.shape[0]
    # ������ȡ����ͼƬ��
    width = gray_1.shape[1]
    # ����ɫ����
    white_max = 0
    # ����ɫ����
    black_max = 0
    # ����ÿһ�еĺڰ�ɫ�����ܺ�
    for i in range(width):
        s = 0  # ��һ�а�ɫ����
        t = 0  # ��һ�к�ɫ����
        for j in range(height):
            if gray_1[j][i] == 255:
                s += 1
            if gray_1[j][i] == 0:
                t += 1
        white_max = max(white_max, s)
        black_max = max(black_max, t)
        white.append(s)
        black.append(t)

    # �ҵ��ұ߽�

    def find_end(start):
        end = start + 1
        for m in range(start + 1, width - 1):
            # ����ȫ�ڵ�����Ϊ�߽�
            if black[m] >= black_max * 0.95:  # 0.95�����������������Ӧ�����0.05
                end = m
                break
        return end

    # ��ʱ����
    n = 1

    # ��ʼλ��
    start = 1

    # ����λ��
    end = 2

    # �ָ�������
    num = 0

    # �ָ���
    res = []

    # ����ָ���·��,��ͼƬ������
    output_path = output_dir + car.split('.')[0]
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # ��������ұ߱���
    while n < width - 2:
        n += 1

        # �ҵ���ɫ��Ϊȷ����ʼ��ַ
        # ������ֱ�� white[n] > white_max
        if white[n] > 0.05 * white_max:
            start = n
            # �ҵ���������
            end = find_end(start)
            # ��һ������ʼ��ַ
            n = end

            # ȷ���ҵ����Ƿ���Ҫ���,��С���ǳ��ƺ�
            if end - start > 10:
                # �ָ�
                char = gray_1[1:height, start - 5:end + 5]
                # ����ָ������ļ�
                cv2.imwrite(output_path+'/' + str(num) + '.jpg', char)
                num += 1
                # ���»��ƴ�С
                char = cv2.resize(char, (300, 300),
                                  interpolation=cv2.INTER_CUBIC)
                # ��ӵ��������
                res.append(char)

                # cv2.imshow("imgStack", char)
                # cv2.waitKey(0)

    # ������Ԫ�淽����չʾ
    res2 = (res[:2], res[2:4], res[4:6], res[6:])
    # ��ʾ���
    imgStack = stackImages(0.5, res2)
    cv2.imshow("imgStack", imgStack)
    cv2.waitKey(0)
