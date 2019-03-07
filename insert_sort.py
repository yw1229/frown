import random


def insert_sort(li):
    for i in range(1, len(li)):  # i表示摸到牌的下标
        tmp = li[i]  # 摸到的牌
        j = i - 1

        while j >= 0 and li[j] > tmp:  # 只要往后挪就循环 2 个条件都得满足
            # 如果j=-1 停止挪 如果li[j]小了 停止挪
            li[j + 1] = li[j]
            j -= 1
        li[j + 1] = tmp
    return li


li = list(range(100))
random.shuffle(li)
print(insert_sort(li))
