with open('inputs/d14.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

# Parse rocks
rocks = set()
max_y = 0
for line in lines:
  points = line.split('->')

  for i in range(len(points) - 1):
    p0 = (int(points[i].split(',')[0]),     int(points[i].split(',')[1]))
    p1 = (int(points[i + 1].split(',')[0]), int(points[i + 1].split(',')[1]))

    # Update maximum y in rocks
    if max(p0[1], p1[1]) > max_y:
      max_y = max(p0[1], p1[1])

    vertical = p0[0] == p1[0]

    if vertical:
      for y in range(min(p0[1], p1[1]), max(p0[1], p1[1]) + 1):
        rocks.add((p0[0], y))
    else:
      for x in range(min(p0[0], p1[0]), max(p0[0], p1[0]) + 1):
        rocks.add((x, p0[1]))

# None if can't move down anymore, coordinates otherwise
def next_move(pos, rocks, sands, floor):
  if pos[1] + 1 >= floor:
    return None

  down   = (pos[0],     pos[1] + 1)
  down_l = (pos[0] - 1, pos[1] + 1)
  down_r = (pos[0] + 1, pos[1] + 1)

  if down not in rocks and down not in sands:
    return down
  elif down_l not in rocks and down_l not in sands:
    return down_l
  elif down_r not in rocks and down_r not in sands:
    return down_r

  return None

# Keep track of sand's path until it settles, start next simulation
# from one time step in the past
def solution(rocks, max_y):
  sands = set()
  path  = [(500, 0)]
  floor = max_y + 2

  found_silver = False
  silver       = 0

  while path:
    curr_pos = path[-1]

    # Voided out (silver solution)
    if not found_silver and curr_pos[1] >= max_y:
      found_silver = True
      silver       = len(sands)

    # Hasn't hit anything yet
    if curr_pos not in rocks and curr_pos not in sands:
      move = next_move(curr_pos, rocks, sands, floor)

      # If it has no possible next moves, pop position and continue
      # simulation from one step before
      if not move:
        sands.add(curr_pos)
        path.pop()
      # Otherwise, add this point to the path for the next grain of sand
      else:
        path.append(move)

  return (silver, len(sands))

silver, gold = solution(rocks, max_y)
print(silver)
print(gold)
