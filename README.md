#俩个栈实现一个队列
入队：元素进栈A

出队：先判断栈B是否为空，为空则将栈A中的元素 pop 出来并 push 进栈B，再栈B出栈，如不为空则栈B直接出栈

复杂度分析：

这样用两个栈实现一个队列,入队的复杂度为O(1)，出队的复杂度则变为O(n)。

而直接用 python 的单个列表实现队列，以列表首作为队列尾，则入队用insert，复杂度为O(n)，出队用pop，复杂度为O(1)。（列表首，即列表中下标为0的元素）


两个队列实现一个栈
进栈：元素入队列A

出栈：判断如果队列A只有一个元素，则直接出队。否则，把队A中的元素出队并入队B，直到队A中只有一个元素，再直接出队。为了下一次继续操作，互换队A和队B。

复杂度分析：

第一种形式：如果以列表尾作为队尾，直接用 append 插入新元素，复杂度为O(1)。

再用pop去弹出队首，也就是列表第0个元素，弹出后插入到另一个队列中。第一次 pop，需要移动列表后面n-1个元素，第二次 pop，需要移动后面n-2个元素……直到最后只剩最后一个元素，直接出队。

复杂度：(n-1)+(n-2)+……+1=O(n^2)。

第二种形式：如果以列表首作为队尾，用 insert 插入新元素，需要移动后面的元素，复杂度则为O(n)。

再用pop去弹出队首，也就是列表最后一个元素，弹出后插入到另一个队列中。这样操作虽然弹出元素的复杂度为O(1)，但再插入另一个队列的复杂度则为O(n)，因为要连续弹出n-1个元素，则需要连续插入n-1个元素，最后的复杂度同样会是O(n^2)。

因此选择第一种形式。

而直接用python的一个列表实现栈，以列表尾为栈首，则出栈和进栈的复杂度都为O(1)。

实现：就以列表作为队列的底层实现，只要保证先进先出的约束就是队列。这里只实现进栈和出栈两个操作。

原文：https://blog.csdn.net/songyunli1111/article/details/79348034 
