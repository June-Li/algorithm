#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [],
    "explicit_horizontal_lines": [],
    "snap_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 5,
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
    "keep_blank_chars": False,
    "text_tolerance": 3,
    "text_x_tolerance": None,
    "text_y_tolerance": None,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": 2,
    "intersection_y_tolerance": 2
}

X_TOLERANCE = 3
PARA_TOLERANCE_PERCENT = 0.05 # 分段参考的句子长度比例
PAGE_PARA_TOLERANCE_PERCENT = 0.8 # 页面分段右边界的最大比例
PAGENUM_TOLERANCE = 0.1 # 在页面末尾10%以后
HEADER_TOLERANCE = 0.1 # 在页面末尾10%以后
LINE_CHAR_TOLERANCE = 3 # 段间距
