import random


# def _quick_sort(li, left, right):
#     if left < right:  # 待排序的区域至少有两个元素
#         mid = partition(li, left, right)  # li 0 6
#         print(mid)
#         _quick_sort(li, left, mid - 1) # 0,3
#         _quick_sort(li, mid + 1, right)
#     return li
#
#
# def partition(li, left, right):  # li 0 5
#     tmp = li[left]  # 8
#     while left < right:  # 0<5 and 22>8
#         while left < right and li[right] >= tmp:
#             right -= 1  # 3
#         li[left] = li[right]  #
#         while left < right and li[left] <= tmp:  #
#             left += 1  # 4
#         li[right] = li[left]
#     li[left] = tmp
#     return left
#


# random.shuffle(li)

# print(_quick_sort(li, 0, len(li) - 1))
def quick_sort(li, left, right):
    if left < right:
        mid = partition(li, left, right)
        quick_sort(li, left, mid - 1)
        quick_sort(li, mid + 1, right)
    return li


def partition(li, left, right):
    tmp = li[left]
    # li = [5, 3, 2, 7, 1, 9, 8]
    while left < right:
        while left < right and li[right] >= tmp:
            right -= 1
        li[left] = li[right]
        while left < right and li[left] <= tmp:
            left += 1
        li[right] = li[left]
        li[left] = tmp
    return left


li = [5, 3, 2, 7, 1, 9, 8]
print(quick_sort(li, 0, len(li) - 1))
