with open('inputs/d1.txt') as in_f:
  lines = in_f.readlines()

elves      = []
curr_cals  = 0
for line in lines:
  line = line.strip()
  if not line:
    elves.append(curr_cals)
    curr_cals = 0
  else:
    curr_cals += int(line)

elves.append(curr_cals)

elves = sorted(elves, reverse=True)

# Silver star
print(elves[0])
# Gold star
print(sum(elves[:3]))
