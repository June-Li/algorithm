import cv2
import numpy as np


def line_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 1)
    bw = cv2.bitwise_not(bw)

    horizontal = bw.copy()
    vertical = bw.copy()

    # [horizontal lines]
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (29, 1))

    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)

    horizontal = cv2.dilate(horizontal, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=3)
    # horizontal = cv2.erode(horizontal, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=1)
    # horizontal = cv2.dilate(horizontal, (1, 1), iterations=5)
    # horizontal = cv2.erode(horizontal, (1, 1), iterations=3)
    # cv2.imshow('horizontal', horizontal)
    # cv2.waitKey()

    hor_lines = cv2.HoughLinesP(horizontal, rho=1, theta=np.pi / 180, threshold=20, minLineLength=20, maxLineGap=3)

    if hor_lines is None:
        return None, None
    temp_line = []
    for line in hor_lines:
        for x1, y1, x2, y2 in line:
            temp_line.append([x1, y1 - 5, x2, y2 - 5])

    hor_lines = sorted(temp_line, key=lambda x: x[1])

    # Selection of best lines from all the horizontal lines detected
    lasty1 = -111111
    lines_x1 = []
    lines_x2 = []
    hor = []
    i = 0
    for x1, y1, x2, y2 in hor_lines:
        if y1 >= lasty1 and y1 <= lasty1 + 10:
            lines_x1.append(x1)
            lines_x2.append(x2)
        else:
            if (i != 0 and len(lines_x1) is not 0):
                hor.append([min(lines_x1), lasty1, max(lines_x2), lasty1])
            lasty1 = y1
            lines_x1 = []
            lines_x2 = []
            lines_x1.append(x1)
            lines_x2.append(x2)
            i += 1
    hor.append([min(lines_x1), lasty1, max(lines_x2), lasty1])

    # [vertical lines]
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 29))

    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    vertical = cv2.dilate(vertical, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=3)
    # vertical = cv2.erode(vertical, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=1)
    # vertical = cv2.dilate(vertical, (1, 1), iterations=9)
    # vertical = cv2.erode(vertical, (1, 1), iterations=3)
    # cv2.imwrite('./buffer/vv.jpg', vertical)
    # cv2.imshow('vertical', vertical)
    # cv2.waitKey()

    ver_lines = cv2.HoughLinesP(vertical, 1, np.pi / 180, 20, np.array([]), 20, 2)

    if ver_lines is None:
        return None, None
    temp_line = []
    for line in ver_lines:
        for x1, y1, x2, y2 in line:
            temp_line.append([x1, y1, x2, y2])

    # Sorting the list of detected lines by X1
    ver_lines = sorted(temp_line, key=lambda x: x[0])

    ## Selection of best lines from all the vertical lines detected ##
    lastx1 = -111111
    lines_y1 = []
    lines_y2 = []
    ver = []
    count = 0
    lasty1 = -11111
    lasty2 = -11111
    for x1, y1, x2, y2 in ver_lines:
        if x1 >= lastx1 and x1 <= lastx1 + 15 and not (
                ((min(y1, y2) < min(lasty1, lasty2) - 20 or min(y1, y2) < min(lasty1, lasty2) + 20)) and (
                (max(y1, y2) < max(lasty1, lasty2) - 20 or max(y1, y2) < max(lasty1, lasty2) + 20))):
            lines_y1.append(y1)
            lines_y2.append(y2)
            # lasty1 = y1
            # lasty2 = y2
        else:
            if (count != 0 and len(lines_y1) is not 0):
                ver.append([lastx1, min(lines_y2) - 5, lastx1, max(lines_y1) - 5])
            lastx1 = x1
            lines_y1 = []
            lines_y2 = []
            lines_y1.append(y1)
            lines_y2.append(y2)
            count += 1
            lasty1 = -11111
            lasty2 = -11111
    ver.append([lastx1, min(lines_y2) - 5, lastx1, max(lines_y1) - 5])

    return hor, ver
