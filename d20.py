with open('inputs/d20.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

class Node:
  def __init__(self, value):
    self.v = value
    self.n = None
    self.p = None

  def preprocess(self, length):
    self.m = self.__get_mod_movement(abs(self.v), length)

  def __get_mod_movement(self, val, length):
    if val < length:
      return val

    ret = 0
    while val > length:
      ret += val % length
      val  = val // length
    return ret + val

  def get_shift_pos(self, length):
    movement   = self.m
    move_right = self.v >= 0

    if not move_right:
      movement -= 1

    new_next = self.n if move_right else self.p
    for _ in range(movement):
      new_next  = new_next.n if move_right else new_next.p
    return new_next

class Ring:
  def __init__(self):
    self.head = None
    self.tail = None
    self.zero = None
    self.size = 0

  def add(self, node):
    if node.v == 0:
      self.zero = node

    if not self.head:
      self.head = node
      self.tail = node
      node.n    = node
      node.p    = node

    node.n = self.head
    node.p = self.tail
    self.tail.n = node
    self.head.p = node
    self.tail   = node

    self.size += 1

  def shift(self, node):
    if not self.head or self.size == 1:
      return

    curr = self.head
    while curr != node:
      curr = curr.n

    # We're shifting the ends
    if curr == self.head:
      self.head = curr.n
    elif curr == self.tail:
      self.tail = curr.p

    # Tie hole left behind by curr
    curr.p.n = curr.n
    curr.n.p = curr.p

    # Get new right neighbor
    new_n = curr.get_shift_pos(self.size)

    # Special case for inserting between head and tail
    if new_n == self.head:
      node.n = self.head
      node.p = self.tail
      self.tail.n = node
      self.head.p = node
      self.tail   = node
    else:
      node.n   = new_n
      node.p   = new_n.p
      node.p.n = node
      node.n.p = node

  def get_val(self, idx):
    start = self.zero
    for _ in range(idx % self.size):
      start = start.n
    return start.v

# Build lists
silver_nodes = []
gold_nodes   = []
silver_file  = Ring()
gold_file    = Ring()
for line in lines:
  silver_node = Node(int(line))
  silver_nodes.append(silver_node)
  silver_file.add(silver_node)
  gold_node   = Node(int(line) * 811589153)
  gold_nodes.append(gold_node)
  gold_file.add(gold_node)

# Get movement steps just once
for s, g in zip(silver_nodes, gold_nodes):
  s.preprocess(silver_file.size)
  g.preprocess(gold_file.size)

# Silver
for node in silver_nodes:
  silver_file.shift(node)
print(sum([silver_file.get_val(x * 1000) for x in range(1, 4)]))

# Gold
for _ in range(10):
  for node in gold_nodes:
    gold_file.shift(node)
print(sum([gold_file.get_val(x * 1000) for x in range(1, 4)]))
