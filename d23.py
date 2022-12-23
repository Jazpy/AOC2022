from collections import defaultdict

with open('inputs/d23.txt', 'r') as in_f:
  lines = [line for line in in_f.readlines()]

class vec2:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def add_new(self, o):
    return vec2(self.x + o.x, self.y + o.y)

  def add(self, o):
    self.x += o.x
    self.y += o.y

  def get_adj(self):
    ret = []
    for i in range(-1, 2):
      for j in range(-1, 2):
        if i == 0 and j == 0:
          continue
        ret.append(self.add_new(vec2(i, j)))
    return ret

  def __eq__(self, o):
    return self.x == o.x and self.y == o.y

  def __hash__(self):
    return hash((self.x, self.y))

class Elf:
  dir_map   = {'N': vec2(0, -1), 'E': vec2( 1, 0),
               'S': vec2(0,  1), 'W': vec2(-1, 0)}
  proposals = [('N', 'NE', 'NW'), ('S', 'SE', 'SW'),
               ('W', 'NW', 'SW'), ('E', 'NE', 'SE')]

  def __init__(self, x, y):
    self.pos = vec2(x, y)

  def __get_adjacent(self):
    return self.pos.get_adj()

  def consider(self, r, elf_positions):
    # Check if moving at all
    adjs   = self.__get_adjacent()
    moving = False
    for adj in adjs:
      if adj in elf_positions:
        moving = True
        break

    if not moving:
      return None

    # Check where we're moving to
    proposal_start = r % len(Elf.proposals)
    for i in range(4):
      proposal = Elf.proposals[(proposal_start + i) % len(Elf.proposals)]

      empty = True
      for d in proposal:
        check = vec2(self.pos.x, self.pos.y)
        for c in d:
          check.add(Elf.dir_map[c])
        if check in elf_positions:
          empty = False
          break
      if empty:
        return self.pos.add_new(Elf.dir_map[proposal[0]])

    return None

# Parsing
elves = []
for y in range(len(lines)):
  line = lines[y]
  for x in range(len(line)):
    if line[x] == '#':
      elves.append(Elf(x, y))

def simulate(elves):
  elf_positions = set()
  for elf in elves:
    elf_positions.add(elf.pos)

  r = 0
  elfs_moved = True

  while elfs_moved:
    elfs_moved      = False
    round_proposals = defaultdict(lambda: [])

    # First half
    for i, elf in enumerate(elves):
      move = elf.consider(r, elf_positions)
      # This elf's not moving
      if not move:
        continue
      round_proposals[move].append(i)
    # Second half
    for p, es in round_proposals.items():
      if len(es) > 1:
        continue
      elfs_moved = True
      e = elves[es[0]]
      elf_positions.remove(e.pos)
      e.pos = p
      elf_positions.add(e.pos)

    # Silver
    if r == 9:
      min_x = min(elf_positions, key=lambda e: e.x).x
      max_x = max(elf_positions, key=lambda e: e.x).x
      min_y = min(elf_positions, key=lambda e: e.y).y
      max_y = max(elf_positions, key=lambda e: e.y).y

      free = 0
      for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
          if vec2(x, y) not in elf_positions:
            free += 1

    r += 1

  return (free, r)

# Solutions
silver, gold = simulate(elves)
print(silver)
print(gold)
