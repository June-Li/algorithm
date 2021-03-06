"""
题目：
    给定一个整数数组nums,请编写一个能够返回数组“中心下标”的方法。
    中心下标是数组的一个下标，其左侧所有元素相加的和等于右侧所有元素相加的和。
    如果数组不存在中心下标，返回-1。如果数组有多个中心下标，应该返回最靠近左边的
    那一个。
    注意:中心下标可能出现在数组的两端。
eg：
    {1, 7, 3, 6, 5, 6}=3
方法：
    1. 左右指针，左指针记录下标左边的和，右指针记录下标右边的和；
    2. 2*sum+current=total
"""