def brace_match(s):
    stack = []
    d = {'(': ')', '[': ']', '{': '}'}
    for ch in s:
        if ch in {'(', '{', '['}:
            stack.append(ch)
        elif len(stack) == 0:
            print('多了右括号%s' % ch)
            return False
        elif d[stack[-1]] == ch:
            stack.pop()

        else:
            print('括号%s处不匹配' % ch)
            return False

    if len(stack) == 0:
        return True
    else:
        print("剩余左括号未匹配")
        return False


print(brace_match('[]{{}[]{()}}'))
