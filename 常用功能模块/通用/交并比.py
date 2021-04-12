def cal_iou(box_1, box_2):
    iou, overlap_area = 0, 0
    min_x = min(box_1[0], box_1[2], box_2[0], box_2[2])
    max_x = max(box_1[0], box_1[2], box_2[0], box_2[2])
    min_y = min(box_1[1], box_1[3], box_2[1], box_2[3])
    max_y = max(box_1[1], box_1[3], box_2[1], box_2[3])
    box_1_w = abs(box_1[0] - box_1[2])
    box_1_h = abs(box_1[1] - box_1[3])
    box_2_w = abs(box_2[0] - box_2[2])
    box_2_h = abs(box_2[1] - box_2[3])
    merge_w = max_x - min_x
    merge_h = max_y - min_y
    overlap_w = box_1_w + box_2_w - merge_w
    overlap_h = box_1_h + box_2_h - merge_h
    if overlap_h > 0 and overlap_w > 0:
        box_1_area = box_1_w * box_1_h
        box_2_area = box_2_w * box_2_h
        overlap_area = overlap_w * overlap_h
        iou = overlap_area / (box_1_area + box_2_area - overlap_area)
    return iou


iou = cal_iou([0, 0, 100, 100], [0, 0, 50, 50])
print(iou)
