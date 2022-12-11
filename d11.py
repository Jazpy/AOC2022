from collections import deque

with open('inputs/d11.txt') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

class Monkey:
  def __init__(self, idx,item_line, op_line, div_line, true_line, false_line):
    self.queue = deque()
    self.idx   = idx

    # Parse items
    for item in item_line.split(':')[1].split(','):
      self.queue.append(int(item))
    # Parse operation
    op_toks = op_line.split('=')[1].split()
    if op_toks[1] == '+':
      if op_toks[2] == 'old':
        self.rule = lambda x : (x + x)
      else:
        self.rule = lambda x : (x + int(op_toks[2]))
    if op_toks[1] == '*':
      if op_toks[2] == 'old':
        self.rule = lambda x : (x * x)
      else:
        self.rule = lambda x : (x * int(op_toks[2]))
    # Parse div test
    self.test = int(div_line.split()[-1])
    # Parse monkeys to throw to
    self.t_monkey = int(true_line.split()[-1])
    self.f_monkey = int(false_line.split()[-1])

    # Monkey business
    self.business = 0

  def has_objects(self):
    return len(self.queue) > 0

  def get_throw(self, diminish=None):
    curr_object    = self.queue.popleft()
    curr_object    = self.rule(curr_object)

    if diminish:
      curr_object = curr_object % diminish
    else:
      curr_object = curr_object // 3

    self.business += 1

    if curr_object % self.test == 0:
      return (self.t_monkey, curr_object)
    else:
      return (self.f_monkey, curr_object)

  def add_object(self, obj):
    self.queue.append(obj)

  def __str__(self):
    return f'Monkey {self.idx}: {self.queue}'

# Parse monkeys
silver_monkeys = []
golden_monkeys = []
line_idx       = 0
while(line_idx < len(lines)):
  curr_line = lines[line_idx]

  if curr_line.startswith('M'):
    silver_monkeys.append(Monkey(len(silver_monkeys), lines[line_idx + 1],
                                 lines[line_idx + 2], lines[line_idx + 3],
                                 lines[line_idx + 4], lines[line_idx + 5]))
    golden_monkeys.append(Monkey(len(golden_monkeys), lines[line_idx + 1],
                                 lines[line_idx + 2], lines[line_idx + 3],
                                 lines[line_idx + 4], lines[line_idx + 5]))

    line_idx += 5

  line_idx += 1


# Silver
for r in range(20):
  for monkey in silver_monkeys:
    while monkey.has_objects():
      throw = monkey.get_throw()
      silver_monkeys[throw[0]].add_object(throw[1])

monkey_business = sorted([m.business for m in silver_monkeys], reverse=True)
print(monkey_business[0] * monkey_business[1])

# Gold
golden_mod = 1
for monkey in golden_monkeys:
  golden_mod *= monkey.test

for r in range(10000):
  for monkey in golden_monkeys:
    while monkey.has_objects():
      throw = monkey.get_throw(golden_mod)
      golden_monkeys[throw[0]].add_object(throw[1])

monkey_business = sorted([m.business for m in golden_monkeys], reverse=True)
print(monkey_business[0] * monkey_business[1])
