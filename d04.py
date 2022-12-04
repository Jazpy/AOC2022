with open('inputs/d04.txt') as in_f:
  lines = in_f.readlines()

silver = 0
gold   = 0
for line in lines:
  elves = line.split(',')

  e0 = elves[0].split('-')
  e1 = elves[1].split('-')

  b0 = int(e0[0])
  b1 = int(e0[1])
  b2 = int(e1[0])
  b3 = int(e1[1])

  min_b = min(b0, b2)
  max_b = max(b1, b3)

  if ((min_b == b0 and max_b == b1) or
      (min_b == b2 and max_b == b3)):
    silver += 1

  if b0 <= b3 and b2 <= b1:
    gold   += 1

print(silver)
print(gold)
