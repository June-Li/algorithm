import cv2
import numpy as np
import os

"""
v0:
"""
# def line_detection(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 1)
#     bw = cv2.bitwise_not(bw)
#     ## To visualize image after thresholding ##
#     # cv2.imshow("bw",bw)
#     # cv2.waitKey(0)
#     ###########################################
#     horizontal = bw.copy()
#     vertical = bw.copy()
#     img = image.copy()
#     # [horizontal lines]
#     # Create structure element for extracting horizontal lines through morphology operations
#     horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
#
#     # Apply morphology operations
#     horizontal = cv2.erode(horizontal, horizontalStructure)
#     horizontal = cv2.dilate(horizontal, horizontalStructure)
#
#     horizontal = cv2.dilate(horizontal, (1,1), iterations=5)
#     horizontal = cv2.erode(horizontal, (1,1), iterations=5)
#
#     ## Uncomment to visualize highlighted Horizontal lines
#     # cv2.imshow("horizontal",horizontal)
#     # cv2.waitKey(0)
#
#     # HoughlinesP function to detect horizontal lines
#     hor_lines = cv2.HoughLinesP(horizontal,rho=1,theta=np.pi/180,threshold=100,minLineLength=30,maxLineGap=3)
#     if hor_lines is None:
#         return None,None
#     temp_line = []
#     for line in hor_lines:
#         for x1,y1,x2,y2 in line:
#             temp_line.append([x1,y1-5,x2,y2-5])
#
#     # Sorting the list of detected lines by Y1
#     hor_lines = sorted(temp_line,key=lambda x: x[1])
#
#     ## Uncomment this part to visualize the lines detected on the image ##
#     # print(len(hor_lines))
#     # for x1, y1, x2, y2 in hor_lines:
#     #     cv2.line(image, (x1,y1), (x2,y2), (0, 255, 0), 1)
#
#
#     # print(image.shape)
#     # cv2.imshow("image",image)
#     # cv2.waitKey(0)
#     ####################################################################
#
#     ## Selection of best lines from all the horizontal lines detected ##
#     lasty1 = -111111
#     lines_x1 = []
#     lines_x2 = []
#     hor = []
#     i=0
#     for x1,y1,x2,y2 in hor_lines:
#         if y1 >= lasty1 and y1 <= lasty1 + 10:
#             lines_x1.append(x1)
#             lines_x2.append(x2)
#         else:
#             if (i != 0 and len(lines_x1) is not 0):
#                 hor.append([min(lines_x1),lasty1,max(lines_x2),lasty1])
#             lasty1 = y1
#             lines_x1 = []
#             lines_x2 = []
#             lines_x1.append(x1)
#             lines_x2.append(x2)
#             i+=1
#     hor.append([min(lines_x1),lasty1,max(lines_x2),lasty1])
#     #####################################################################
#
#
#     # [vertical lines]
#     # Create structure element for extracting vertical lines through morphology operations
#     verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
#
#     # Apply morphology operations
#     vertical = cv2.erode(vertical, verticalStructure)
#     vertical = cv2.dilate(vertical, verticalStructure)
#
#     vertical = cv2.dilate(vertical, (1,1), iterations=8)
#     vertical = cv2.erode(vertical, (1,1), iterations=7)
#
#     ######## Preprocessing Vertical Lines ###############
#     # cv2.imshow("vertical",vertical)
#     # cv2.waitKey(0)
#     #####################################################
#
#     # HoughlinesP function to detect vertical lines
#     # ver_lines = cv2.HoughLinesP(vertical,rho=1,theta=np.pi/180,threshold=20,minLineLength=20,maxLineGap=2)
#     ver_lines = cv2.HoughLinesP(vertical, 1, np.pi/180, 20, np.array([]), 20, 2)
#     if ver_lines is None:
#         return None,None
#     temp_line = []
#     for line in ver_lines:
#         for x1,y1,x2,y2 in line:
#             temp_line.append([x1,y1,x2,y2])
#
#     # Sorting the list of detected lines by X1
#     ver_lines = sorted(temp_line,key=lambda x: x[0])
#
#     ## Uncomment this part to visualize the lines detected on the image ##
#     # print(len(ver_lines))
#     # for x1, y1, x2, y2 in ver_lines:
#     #     cv2.line(image, (x1,y1-5), (x2,y2-5), (0, 255, 0), 1)
#
#
#     # print(image.shape)
#     # cv2.imshow("image",image)
#     # cv2.waitKey(0)
#     ####################################################################
#
#     ## Selection of best lines from all the vertical lines detected ##
#     lastx1 = -111111
#     lines_y1 = []
#     lines_y2 = []
#     ver = []
#     count = 0
#     lasty1 = -11111
#     lasty2 = -11111
#     for x1,y1,x2,y2 in ver_lines:
#         if x1 >= lastx1 and x1 <= lastx1 + 15 and not (((min(y1,y2)<min(lasty1,lasty2)-20 or min(y1,y2)<min(lasty1,lasty2)+20)) and ((max(y1,y2)<max(lasty1,lasty2)-20 or max(y1,y2)<max(lasty1,lasty2)+20))):
#             lines_y1.append(y1)
#             lines_y2.append(y2)
#             # lasty1 = y1
#             # lasty2 = y2
#         else:
#             if (count != 0 and len(lines_y1) is not 0):
#                 ver.append([lastx1,min(lines_y2)-5,lastx1,max(lines_y1)-5])
#             lastx1 = x1
#             lines_y1 = []
#             lines_y2 = []
#             lines_y1.append(y1)
#             lines_y2.append(y2)
#             count += 1
#             lasty1 = -11111
#             lasty2 = -11111
#     ver.append([lastx1,min(lines_y2)-5,lastx1,max(lines_y1)-5])
#     #################################################################
#
#
#     ############ Visualization of Lines After Post Processing ############
#     # for x1, y1, x2, y2 in ver:
#     #     cv2.line(img, (x1,y1), (x2,y2), (0, 255, 0), 1)
#
#     # for x1, y1, x2, y2 in hor:
#     #     cv2.line(img, (x1,y1), (x2,y2), (0, 255, 0), 1)
#
#     # cv2.imshow("image",img)
#     # cv2.waitKey(0)
#     #######################################################################
#
#     return hor,ver

# line_detection(cv2.imread('path to image'))


"""
v1:
"""
# def line_detection(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 1)
#     bw = cv2.bitwise_not(bw)
#     ## To visualize image after thresholding ##
#     # cv2.imshow("bw",bw)
#     # cv2.waitKey(0)
#     ###########################################
#     horizontal = bw.copy()
#     vertical = bw.copy()
#     img = image.copy()
#     # [horizontal lines]
#     # Create structure element for extracting horizontal lines through morphology operations
#     horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (29, 1))
#
#     # Apply morphology operations
#     horizontal = cv2.erode(horizontal, horizontalStructure)
#     horizontal = cv2.dilate(horizontal, horizontalStructure)
#
#     # horizontal = cv2.dilate(horizontal, (1, 1), iterations=5)
#     # horizontal = cv2.erode(horizontal, (1, 1), iterations=3)
#     horizontal = cv2.dilate(horizontal, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=3)
#     # horizontal = cv2.erode(horizontal, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=1)
#     cv2.imshow('horizontal', horizontal)
#     cv2.waitKey()
#
#     ## Uncomment to visualize highlighted Horizontal lines
#     # cv2.imshow("horizontal",horizontal)
#     # cv2.waitKey(0)
#
#     # HoughlinesP function to detect horizontal lines
#     hor_lines = cv2.HoughLinesP(horizontal, rho=1, theta=np.pi / 180, threshold=20, minLineLength=20, maxLineGap=3)
#     # hor_lines = cv2.HoughLinesP(horizontal, 1, np.pi / 180, 20, np.array([]), 20, 2)
#     if hor_lines is None:
#         return None, None
#     temp_line = []
#     for line in hor_lines:
#         for x1, y1, x2, y2 in line:
#             temp_line.append([x1, y1 - 5, x2, y2 - 5])
#
#     # Sorting the list of detected lines by Y1
#     hor_lines = sorted(temp_line, key=lambda x: x[1])
#
#     ## Uncomment this part to visualize the lines detected on the image ##
#     # print(len(hor_lines))
#     # for x1, y1, x2, y2 in hor_lines:
#     #     cv2.line(image, (x1,y1), (x2,y2), (0, 255, 0), 1)
#
#     # print(image.shape)
#     # cv2.imshow("image",image)
#     # cv2.waitKey(0)
#     ####################################################################
#
#     ## Selection of best lines from all the horizontal lines detected ##
#     lasty1 = -111111
#     lines_x1 = []
#     lines_x2 = []
#     hor = []
#     i = 0
#     for x1, y1, x2, y2 in hor_lines:
#         if y1 >= lasty1 and y1 <= lasty1 + 10:
#             lines_x1.append(x1)
#             lines_x2.append(x2)
#         else:
#             if (i != 0 and len(lines_x1) is not 0):
#                 hor.append([min(lines_x1), lasty1, max(lines_x2), lasty1])
#             lasty1 = y1
#             lines_x1 = []
#             lines_x2 = []
#             lines_x1.append(x1)
#             lines_x2.append(x2)
#             i += 1
#     hor.append([min(lines_x1), lasty1, max(lines_x2), lasty1])
#     #####################################################################
#
#     # [vertical lines]
#     # Create structure element for extracting vertical lines through morphology operations
#     verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 29))
#
#     # Apply morphology operations
#     vertical = cv2.erode(vertical, verticalStructure)
#     vertical = cv2.dilate(vertical, verticalStructure)
#
#     # vertical = cv2.dilate(vertical, (1, 1), iterations=9)
#     # vertical = cv2.erode(vertical, (1, 1), iterations=3)
#     vertical = cv2.dilate(vertical, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=3)
#     # vertical = cv2.erode(vertical, cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)), iterations=1)
#     cv2.imshow('vertical', vertical)
#     cv2.waitKey()
#
#     ######## Preprocessing Vertical Lines ###############
#     # cv2.imshow("vertical",vertical)
#     # cv2.waitKey(0)
#     #####################################################
#
#     # HoughlinesP function to detect vertical lines
#     # ver_lines = cv2.HoughLinesP(vertical,rho=1,theta=np.pi/180,threshold=20,minLineLength=20,maxLineGap=2)
#     ver_lines = cv2.HoughLinesP(vertical, 1, np.pi / 180, 20, np.array([]), 20, 2)
#     # ver_lines = np.concatenate(ver_lines, cv2.HoughLinesP(vertical, 1, np.pi / 180, 3, np.array([]), 20, 2))
#     if ver_lines is None:
#         return None, None
#     temp_line = []
#     for line in ver_lines:
#         for x1, y1, x2, y2 in line:
#             temp_line.append([x1, y1, x2, y2])
#
#     # Sorting the list of detected lines by X1
#     ver_lines = sorted(temp_line, key=lambda x: x[0])
#
#     ## Uncomment this part to visualize the lines detected on the image ##
#     # print(len(ver_lines))
#     # for x1, y1, x2, y2 in ver_lines:
#     #     cv2.line(image, (x1,y1-5), (x2,y2-5), (0, 255, 0), 1)
#
#     # print(image.shape)
#     # cv2.imshow("image",image)
#     # cv2.waitKey(0)
#     ####################################################################
#
#     ## Selection of best lines from all the vertical lines detected ##
#     lastx1 = -111111
#     lines_y1 = []
#     lines_y2 = []
#     ver = []
#     count = 0
#     lasty1 = -11111
#     lasty2 = -11111
#     for x1, y1, x2, y2 in ver_lines:
#         if x1 >= lastx1 and x1 <= lastx1 + 15 and not (
#                 ((min(y1, y2) < min(lasty1, lasty2) - 20 or min(y1, y2) < min(lasty1, lasty2) + 20)) and (
#                 (max(y1, y2) < max(lasty1, lasty2) - 20 or max(y1, y2) < max(lasty1, lasty2) + 20))):
#             lines_y1.append(y1)
#             lines_y2.append(y2)
#             # lasty1 = y1
#             # lasty2 = y2
#         else:
#             if (count != 0 and len(lines_y1) is not 0):
#                 ver.append([lastx1, min(lines_y2) - 5, lastx1, max(lines_y1) - 5])
#             lastx1 = x1
#             lines_y1 = []
#             lines_y2 = []
#             lines_y1.append(y1)
#             lines_y2.append(y2)
#             count += 1
#             lasty1 = -11111
#             lasty2 = -11111
#     ver.append([lastx1, min(lines_y2) - 5, lastx1, max(lines_y1) - 5])
#     #################################################################
#
#     ############ Visualization of Lines After Post Processing ############
#     # for x1, y1, x2, y2 in ver:
#     #     cv2.line(img, (x1,y1), (x2,y2), (0, 255, 0), 1)
#
#     # for x1, y1, x2, y2 in hor:
#     #     cv2.line(img, (x1,y1), (x2,y2), (0, 255, 0), 1)
#
#     # cv2.imshow("image",img)
#     # cv2.waitKey(0)
#     #######################################################################
#
#     return hor, ver


"""
v2：
"""
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


base_path = '/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/doc/my_imgs_11/'
image_name_list = os.listdir(base_path)
for image_name in image_name_list:
    # image = cv2.imread('/Volumes/my_disk/company/sensedeal/项目/POC/华夏国际银行poc需求梳理/样例/20210409/公司章程_jpg/001-00001-嘉记-公司章程/001-00001-嘉记-公司章程_2.jpg')
    image = cv2.imread('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/result/zhangcheng_20210409/001-00001-嘉记-公司章程/001-00001-嘉记-公司章程_2_table_ori_0.jpg')
    # image = cv2.imread('/Volumes/my_disk/company/sensedeal/217_PycharmProject/bbtv/PaddleOCR-1.0-2021/result/zhangcheng_20210409/001-00001-广州海印实业集团有限公司_章程_(1)/001-00001-广州海印实业集团有限公司_章程_(1)_1_table_ori_0.jpg')
    # image = cv2.imread(base_path + image_name)
    img_h, img_w, _ = np.shape(image)
    if img_h > 500:
        resize_h = 500
    else:
        resize_h = img_w
    temp_lines_hor, temp_lines_ver = line_detection(image)
    if temp_lines_hor is None:
        temp_lines_hor = []
    if temp_lines_ver is None:
        temp_lines_ver = []
    temp_lines_hor.append([0, 0, img_w, 0])
    temp_lines_hor.append([0, img_h, img_w, img_h])
    temp_lines_ver.append([0, 0, 0, img_h])
    temp_lines_ver.append([img_w, 0, img_w, img_h])

    temp = []
    sort_list = []
    for line in temp_lines_hor:
        x1, y1, x2, y2 = line
        if abs(x1 - x2) / img_w > 0.5:
            temp.append([x1, y1, x2, y2])
            sort_list.append(y1)
    temp_lines_hor = np.array(temp)[sorted(range(len(sort_list)), key=lambda k: sort_list[k])]

    temp = []
    sort_list = []
    for line in temp_lines_ver:
        x1, y1, x2, y2 = line
        if abs(y1 - y2) / img_h > 0.5:
            temp.append([x1, y1, x2, y2])
            sort_list.append(x1)
    temp_lines_ver = np.array(temp)[sorted(range(len(sort_list)), key=lambda k: sort_list[k])]
    show_image = image.copy()
    for line in temp_lines_hor:
        cv2.line(show_image, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 2)
    for line in temp_lines_ver:
        cv2.line(show_image, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 2)
    # cv2.imshow('show_image', cv2.resize(show_image, (800, 800)))
    cv2.imshow('show_image', show_image)
    cv2.waitKey()
