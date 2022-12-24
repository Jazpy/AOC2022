import numpy as np
from collections import deque

with open('inputs/d24.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

class vec2:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def add_new(self, o):
    return vec2(self.x + o.x, self.y + o.y)

  def add(self, o):
    self.x += o.x
    self.y += o.y

  def step(self, d, x_lim, y_lim):
    ret = self.add_new(d)

    if ret.x < x_lim[0]:
      ret.x = x_lim[1]
    elif ret.x > x_lim[1]:
      ret.x = x_lim[0]
    elif ret.y < y_lim[0]:
      ret.y = y_lim[1]
    elif ret.y > y_lim[1]:
      ret.y = y_lim[0]

    return ret

  def __eq__(self, o):
    if isinstance(o, tuple):
      return (self.x, self.y) == o
    return self.x == o.x and self.y == o.y

  def __hash__(self):
    return hash((self.x, self.y))

class Blizzard:
  dir_map = {'<': vec2(-1, 0), '>': vec2(1, 0),
             '^': vec2(0, -1), 'v': vec2(0, 1)}

  def __init__(self, x, y, d):
    self.dir   = Blizzard.dir_map[d]
    self.pos   = vec2(x, y)

class BlizzardMap:
  def __init__(self, blizzards, x_min, x_max, y_min, y_max):
    self.x_lim = [x_min, x_max]
    self.y_lim = [y_min, y_max]
    self.blizzards = blizzards

    self.time_map    = {}
    self.time_map[0] = set()
    for blizz in blizzards:
      self.time_map[0].add(blizz.pos)

    for i in range(1, 1000):
      self.time_map[i] = set()
      for blizz in blizzards:
        blizz.pos = blizz.pos.step(blizz.dir, self.x_lim, self.y_lim)
        self.time_map[i].add(blizz.pos)

  def hit(self, coords, t):
    return coords in self.time_map[t]

# Parsing
x_min = 1
y_min = 1
x_max = len(lines[0]) - 2
y_max = len(lines)    - 2
walls     = set()
blizzards = []

for y, line in enumerate(lines):
  for x, c in enumerate(line):
    if c == '#':
      walls.add((x, y))
    elif c in '<>^v':
      blizzards.append(Blizzard(x, y, c))

walls.add((1, -1))
walls.add((x_max, y_max + 2))
blizzard_map = BlizzardMap(blizzards, x_min, x_max, y_min, y_max)

# Solution
def get_neighbors(pos, blizzard_map, walls):
  pos_x = pos[0]
  pos_y = pos[1]
  new_t = pos[2] + 1
  possible_moves = [(pos_x + 1, pos_y), (pos_x, pos_y + 1),
                    (pos_x - 1, pos_y), (pos_x, pos_y - 1), (pos_x, pos_y)]
  ret = []
  for move in possible_moves:
    if move not in walls and not blizzard_map.hit(move, new_t):
      ret.append((move[0], move[1], new_t))
  return ret

def bfs(blizzard_map, walls, start, end, x_max, y_max):
  q = deque()
  visited   = np.zeros((x_max, y_max, 1000), dtype=np.int8)
  distances = np.full((x_max, y_max, 1000),
    np.iinfo(np.int32).max, dtype=np.int32)

  visited[start[0], start[1], start[2]] = 1
  distances[start[0], start[1], start[2]] = 0
  q.append(start)

  while q:
    curr = q.popleft()
    neighbors = get_neighbors(curr, blizzard_map, walls)

    for n in neighbors:
      if visited[n[0], n[1], n[2]]:
        continue

      visited[n[0], n[1], n[2]]   = 1
      distances[n[0], n[1], n[2]] = distances[curr[0], curr[1], curr[2]] + 1

      if (n[0], n[1]) == end:
        return distances[n[0], n[1], n[2]]

      q.append(n)

  return 0

# Silver
first_t = bfs(blizzard_map, walls, (1, 0, 0), (x_max, y_max + 1),
  x_max + 1, y_max + 2)
print(first_t)

# Gold
second_t = first_t + bfs(blizzard_map, walls, (x_max, y_max + 1, first_t),
  (1, 0), x_max + 1, y_max + 2)
third_t  = second_t + bfs(blizzard_map, walls, (1, 0, second_t),
  (x_max, y_max + 1), x_max + 1, y_max + 2)
print(third_t)
