with open('inputs/d10.txt') as in_f:
  lines = in_f.readlines()

silver        = 0
cycle_counter = 0
row_position  = 0
register      = 1
instr_stack   = []

lines.reverse()
while lines or instr_stack:
  cycle_counter += 1

  # Gold
  if abs(register - row_position) <= 1:
    print('#', end='')
  else:
    print('.', end='')
  row_position += 1

  if row_position == 40:
    print('')
    row_position = 0

  # Silver
  if cycle_counter == 20 or (cycle_counter - 20) % 40 == 0:
    silver += cycle_counter * register

  if instr_stack:
    register += instr_stack.pop()
  else:
    curr_instr = lines.pop()
    if curr_instr[0] == 'n':
      continue
    else:
      instr_stack.append(int(curr_instr.split()[1]))

# Should also check if cycle is multiple of 40 after loop

print(silver)
