import ast
from functools import cmp_to_key

with open('inputs/d13.txt', 'r') as in_f:
    lines = [line.strip() for line in in_f.readlines()]
lines.append('[[6]]')
lines.append('[[2]]')

def list_cmp(l0, l1):
    idx = 0
    while idx < min(len(l0), len(l1)):
        result = 0

        if isinstance(l0[idx], int) and isinstance(l1[idx], int):
            if l0[idx] < l1[idx]:
                result = -1
            elif l1[idx] < l0[idx]:
                result =  1
        elif isinstance(l0[idx], list) and isinstance(l1[idx], list):
            result = list_cmp(l0[idx], l1[idx])
        elif isinstance(l0[idx], int) and isinstance(l1[idx], list):
            result = list_cmp([l0[idx]], l1[idx])
        elif isinstance(l0[idx], list) and isinstance(l1[idx], int):
            result = list_cmp(l0[idx], [l1[idx]])

        if result != 0:
            return result

        idx += 1

    if len(l0) == len(l1):
        return 0
    elif len(l0) < len(l1):
        return -1
    else:
        return  1

# Parsing
lists = []
for line in lines:
    if not line:
        continue

    # Import solution
    lists.append(ast.literal_eval(line))

# Silver
silver = []
for i in range(0, len(lists), 2):
    # Import solution
    l0 = lists[i]
    l1 = lists[i + 1]

    # Compare pairs
    if list_cmp(l0, l1) < 0:
        silver.append(i // 2 + 1)

print(sum(silver))

# Gold
gold = 1
lists.sort(key=cmp_to_key(list_cmp))
for i, l in enumerate(lists):
    if list_cmp(l, [[2]]) == 0 or list_cmp(l, [[6]]) == 0:
        gold *= i + 1

print(gold)
