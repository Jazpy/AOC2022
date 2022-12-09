with open('inputs/d09.txt') as in_f:
  lines = in_f.readlines()

class Vec2D:
  def __init__(self, x, y, direction=None):
    self.x = x
    self.y = y

    if direction:
      self.x = 0
      self.y = 0

      if direction == 'R':
        self.x =  1
      elif direction == 'L':
        self.x = -1
      elif direction == 'U':
        self.y =  1
      elif direction == 'D':
        self.y = -1

  def add(self, other):
    self.x += other.x
    self.y += other.y

  def get_tuple(self):
    return (self.x, self.y)

  # Diagonal movements have unit cost
  def distance(self, other):
    return max(abs(self.x - other.x), abs(self.y - other.y))
  # Direction to move in
  def direction_to(self, other):
    direction = Vec2D(0, 0)

    if other.x > self.x:
      direction.x =  1
    elif other.x < self.x:
      direction.x = -1

    if other.y > self.y:
      direction.y =  1
    elif other.y < self.y:
      direction.y = -1

    return direction

def gold_solution(lines, length):
  rope = [Vec2D(0, 0) for _ in range(length)]
  head = rope[0]
  tail = rope[-1]
  uniq = set()
  uniq.add(tail.get_tuple())

  for line in lines:
    toks    = line.split()
    in_dir  = toks[0]
    mag     = int(toks[1])
    vec_dir = Vec2D(0, 0, in_dir)

    for i in range(mag):
      head.add(vec_dir)

      prev_knot = head
      for knot in rope[1:]:
        if knot.distance(prev_knot) > 1:
          knot.add(knot.direction_to(prev_knot))
          if knot == tail:
            uniq.add(knot.get_tuple())
        prev_knot = knot

  return len(uniq)

print(gold_solution(lines, 2))
print(gold_solution(lines, 10))
