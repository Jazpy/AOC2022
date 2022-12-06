from collections import deque

def is_unique(num, d):
  uniques = set()
  for c in d:
    uniques.add(c)
  return len(uniques) == num

with open('inputs/d06.txt') as in_f:
  lines = in_f.readlines()

buf = lines[0]
win = deque(buf[:4])

silver = 0
for i in range(4, len(buf)):
  if is_unique(4, win):
    silver = i
    break

  win.popleft()
  win.append(buf[i])

win = deque(buf[silver - 1 : silver + 13])

gold = 0
for i in range(silver + 13, len(buf)):
  if is_unique(14, win):
    gold = i
    break

  win.popleft()
  win.append(buf[i])

print(silver)
print(gold)
