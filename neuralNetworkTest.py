from keras.models import load_model
import cv2 as cv
import numpy as np
import os
import random

img = cv.imread('0.bmp', 0)

imgScale = 2
newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
img = cv.resize(img, (int(newX), int(newY)))
th3 = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)

mx = int((img.shape[0] / 1.1) * (img.shape[1] / 1.1))
img = cv.copyMakeBorder(img, 50, 50, 50, 50, cv.BORDER_CONSTANT, value=(255, 255, 255, 0))
copyimg = img.copy()

contours, hierarchy = cv.findContours(th3, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

colors = [(0, 0, 255),
          (0, 255, 255),
          (0, 255, 0),
          (255, 0, 0)]

crops = {}

for j, cnt in enumerate(contours):
    rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
    box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
    box = np.int0(box)  # округление координат
    area = int(rect[1][0] * rect[1][1])  # вычисление площади
    if mx > area > 1200:
        # print(j, area, rect[1][0], rect[1][1])

        pts2 = np.float32([[0, 23], [0, 0], [104, 0], [104, 23]])
        bxX = []
        bxY = []
        for i in box:
            bxX.append(i[0])
            bxY.append(i[1])

        bxX = sorted(bxX)[2:]
        bxY = sorted(bxY)[2:]

        for i, v in enumerate(box):
            if v[0] in bxX:
                pts2[i][0] = 104
            else:
                pts2[i][0] = 0

            if v[1] in bxY:
                pts2[i][1] = 23
            else:
                pts2[i][1] = 0

        pts1 = np.float32(box + [50, 50])

        M = cv.getPerspectiveTransform(pts1, pts2)

        dst = cv.warpPerspective(img, M, (104, 23))

        crops[str(j)] = dst

model = load_model(r"E:\CropNums\my_model.h5")

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.summary()

for i in crops:
    img_arr = crops[i]
    img_test = img_arr.reshape(-1, 104, 23, 3)
    score = model.predict(img_test)[0][0]
    if score < 0.5:
        print(i, score)
        cv.imshow(i, img_arr)

cv.waitKey(0)
cv.destroyAllWindows()
