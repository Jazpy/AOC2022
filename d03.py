with open('inputs/d03.txt') as in_f:
  lines = in_f.readlines()

def to_int(c):
  if c.islower():
    return ord(c) - 96
  else:
    return ord(c) - 64 + 26

# Silver star
silver = []
for line in lines:
  line = line.strip()
  mid  = len(line) // 2
  dic  = {}

  # Hash first compartment
  for c in line[:mid]:
    dic[c] = 1

  for c in line[mid:]:
    if dic.get(c):
      silver.append(to_int(c))
      break

print(sum(silver))

# Gold star
gold = []
for i in range(0, len(lines), 3):
  l0 = lines[i].strip()
  l1 = lines[i + 1].strip()
  l2 = lines[i + 2].strip()

  dic = {}

  for c0 in l0:
    if not dic.get(c0):
      dic[c0] = 1

  for c1 in l1:
    if dic.get(c1):
      dic[c1] = 2

  for c2 in l2:
    if dic.get(c2) == 2:
      gold.append(to_int(c2))
      break

print(sum(gold))
