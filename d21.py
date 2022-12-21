import sympy

with open('inputs/d21.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

monkeys = {}
for line in lines:
  toks = line.split(':')
  monkeys[toks[0]] = toks[1].strip()

# Evaluation tree
class Node:
  def __init__(self, name, operations):
    self.name = name
    self.leaf = False

    toks = operations[self.name].split()
    if len(toks) == 1:
      self.leaf = True
      self.val  = int(toks[0])
    else:
      self.op    = self.__get_op(toks[1])
      self.left  = Node(toks[0], operations)
      self.right = Node(toks[2], operations)

  def evaluate(self, gold=False):
    if self.name == 'humn' and gold:
      return 'x'
    if self.name == 'root' and gold:
      return f'Eq({self.left.evaluate(gold)}, {self.right.evaluate(gold)})'

    if self.leaf:
      return self.val
    return self.op(self.left.evaluate(gold), self.right.evaluate(gold))

  def __get_op(self, c):
    if c == '+':
      return lambda x, y: x +  y if not isinstance(x, str) and not isinstance(y, str) else f'({x} + {y})'
    if c == '-':
      return lambda x, y: x -  y if not isinstance(x, str) and not isinstance(y, str) else f'({x} - {y})'
    if c == '*':
      return lambda x, y: x *  y if not isinstance(x, str) and not isinstance(y, str) else f'({x} * {y})'
    if c == '/':
      return lambda x, y: x // y if not isinstance(x, str) and not isinstance(y, str) else f'({x} / {y})'

# Build tree
root = Node('root', monkeys)

# Silver
print(root.evaluate())
# Gold, import solution
print(sympy.solve(root.evaluate(gold=True))[0])
