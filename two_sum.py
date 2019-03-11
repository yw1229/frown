# li = [2, 1, 3, 5]
#
#
# def two_sum_1(li, num):
#     for i in range(len(li)):
#         for j in range(i + 1, len(li)):
#             if li[i] + li[j] == num:
#                 return i, j
#
#
# print(two_sum_1(li, 4))


#
#
# def bin_search(li, val, low, high):
#     while low <= high:
#         mid = (low + high) // 2
#         if li[mid] == val:
#             return mid
#         elif li[mid] < val:
#             low = mid + 1
#         else:
#             high = mid - 1
#     return -1
#
# li = [2, 1, 3, 5,]
# # print (bin_search(li, 4, 0, len(li) - 1))
#
# # 要求有序
# def two_sum_2(li, num):
#     for i in range(len(li)):
#         a = li[i]
#         b = num - a
#         j = bin_search(li, b, i + 1, len(li) - 1)
#         if j > 0:
#             return i, j
#
#
# print (two_sum_2(li, 4))


##### 要求有序
def two_sum_3(li, num):
    i = 0
    j = len(li) - 1
    while i < j:
        s = li[i] + li[j]
        if s == num:
            return i, j
        elif s < num:
            i += 1
        elif s > num:
            j -= 1
    return -1, -1


li = [2, 1, 3, 5]
print (two_sum_3(li, 4))


# 不要求有序

def two_sum_4(li, num):
    dic = {}
    for i in range(len(li)):
        a = li[i]
        b = num - li[i]
        if b not in dic:
            dic[a] = i

        else:
            return dic[b], i


print (two_sum_4(li, 4))
# 2-sum问题
# 无序列表: 4哈希表(最优)
# 有序列表: 3两边找(最优)


# 3-sum问题
# 1.暴力枚举法 O(n^3)
# 2.二分查找   O(n^2logn)
# 3.两边找     O(n^2) (最优)
# 4.哈希表     O(n^2) (次优)

# 2-sub问题
# 哈希表    O(n) 定住一个找#两#个