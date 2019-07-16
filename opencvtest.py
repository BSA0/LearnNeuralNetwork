import cv2 as cv
import numpy as np
import os
import random


numspath = r"E:\CropNums\NumBase"
correctpath = r"E:\CropNums\OnlyNums"
wrongpath = r"E:\CropNums\OnlyTrash"

global_wrongi = len(os.listdir(wrongpath))
global_correcti = len(os.listdir(correctpath))

folder = os.listdir(numspath)
mx = len(folder)
for i in range(1000):
    num = random.randint(0, mx)
    img = cv.imread(os.path.join(numspath, folder[num]), 0)

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
            # cv.imshow("Image{}".format(j), dst)

            crops[str(j)] = dst

            # cv.drawContours(th3, [box], 0, (rect[1][1], rect[1][0], 0), 2)
            cv.drawContours(copyimg, [box + [50, 50]], 0, (rect[1][1], rect[1][0], 0), 2)
            for i in range(len(box)):
                cv.circle(copyimg, (box[i][0] + 50, box[i][1] + 50), 3, colors[i], -1)
            cv.putText(copyimg, '{}'.format(j), (box[0][0] + 50, box[0][1] + 50), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                       (64, 64, 64), 1, cv.LINE_AA)

    f = True

    while f:
        cv.imshow("ImageOC", copyimg)
        cv.waitKey(0)
        print(crops.keys())

        command = input()

        if command == 's':
            f = False
            continue

        if command == '-1':
            f = False
            for pic in crops:
                cv.imwrite(os.path.join(wrongpath, 'notnum{}.bmp'.format(global_wrongi)), crops.get(pic))
                global_wrongi += 1
            continue

        if crops.get(command) is not None:
            cv.imshow("Image{}".format(command), crops.get(command))
            cv.waitKey(0)
            cmd = input()
            if cmd == 'y':
                cv.imwrite(os.path.join(correctpath, 'num{}.bmp'.format(global_correcti)), crops.get(command))
                global_correcti += 1
                crops.pop(command)
                f = False
                for pic in crops:
                    cv.imwrite(os.path.join(wrongpath, 'notnum{}.bmp'.format(global_wrongi)), crops.get(pic))
                    global_wrongi += 1
            elif cmd == 'w':
                global_correcti += 1
                crops.pop(command)
                f = False
                for pic in crops:
                    cv.imwrite(os.path.join(wrongpath, 'notnum{}.bmp'.format(global_wrongi)), crops.get(pic))
                    global_wrongi += 1


# cv.imshow("ImageO", img)
# cv.imshow("ImageC", th3)

cv.destroyAllWindows()
