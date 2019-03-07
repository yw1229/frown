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
li = [5, 3, 2, 7, 1, 9, 8]


def quick_sort_one(li):
    if len(li) < 2:
        return li
    tmp = li[0]
    right = [i for i in li[1:] if i >= tmp]
    left = [i for i in li[1:] if i <= tmp]
    right = quick_sort_one(right)
    left = quick_sort_one(left)
    return left + [tmp] + right


print(quick_sort_one(li))
