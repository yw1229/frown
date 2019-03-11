import random

li = [3, 9, 5, 6, 2]


# 取列表里最小元素的下标
def get_min_pos(li):
    min_pos = 0
    for i in range(1, len(li)):
        if li[i] < li[min_pos]:
            min_pos = i
    return min_pos


print (get_min_pos(li))


def select_sort(li):
    for i in range(len(li) - 1):
        # 第i趟无序区范围 i-最后
        min_pos = i  # min_pos更新为无序区最小值位置
        for j in range(i + 1, len(li)):
            if li[j] < li[min_pos]:
                min_pos = j
        li[i], li[min_pos] = li[min_pos], li[i]

    return li


print (select_sort(li))
