with open('inputs/d05.txt') as in_f:
  lines = in_f.readlines()

stack_lines   = lines[:8]
silver_stacks = [[] for n in range(9)]
gold_stacks   = [[] for n in range(9)]

for stack_line in reversed(stack_lines):
  for i in range(9):
    char = stack_line[(i * 4) + 1]

    if char != ' ':
      silver_stacks[i].append(char)
      gold_stacks[i].append(char)

move_lines = lines[10:]

for line in move_lines:
  toks = line.split()

  amount = int(toks[1])
  origin = int(toks[3]) - 1
  dstntn = int(toks[5]) - 1

  # CRATEMOVER 9000
  for _ in range(amount):
    silver_stacks[dstntn].append(silver_stacks[origin].pop())
  # CRATEMOVER 9001
  gold_stacks[dstntn].extend(gold_stacks[origin][-amount:])
  del gold_stacks[origin][-amount:]

print(''.join([s[-1] for s in silver_stacks]))
print(''.join([s[-1] for s in gold_stacks]))
