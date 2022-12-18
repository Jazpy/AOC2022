from itertools import product

with open('inputs/d18.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

cubes = {}
for line in lines:
  toks = line.split(',')
  cubes[(int(toks[0]), int(toks[1]), int(toks[2]))] = 0

# Count faces that are only covered by air (component 1)
def get_uncovered(cubes):
  ret = 0

  for cube in cubes:
    # Only count lava
    if cubes[cube] == 1:
      continue
    # Count and subtract covered faces
    uncovered = 6
    if cubes.get((cube[0] + 1, cube[1], cube[2]), 1) != 1:
      uncovered -= 1
    if cubes.get((cube[0] - 1, cube[1], cube[2]), 1) != 1:
      uncovered -= 1
    if cubes.get((cube[0], cube[1] + 1, cube[2]), 1) != 1:
      uncovered -= 1
    if cubes.get((cube[0], cube[1] - 1, cube[2]), 1) != 1:
      uncovered -= 1
    if cubes.get((cube[0], cube[1], cube[2] + 1), 1) != 1:
      uncovered -= 1
    if cubes.get((cube[0], cube[1], cube[2] - 1), 1) != 1:
      uncovered -= 1

    ret += uncovered

  return ret

# Silver
print(get_uncovered(cubes))

# Gold
def spread_component(cubes, cube, component):
  stack = [cube]

  while stack:
    curr = stack.pop()

    # Only spread to unmarked cubes
    if not curr in cubes or cubes[curr] != -1:
      continue

    cubes[curr] = component
    # X
    stack.append((curr[0] + 1, curr[1],     curr[2]))
    stack.append((curr[0] - 1, curr[1],     curr[2]))
    # Y
    stack.append((curr[0],     curr[1] + 1, curr[2]))
    stack.append((curr[0],     curr[1] - 1, curr[2]))
    # Z
    stack.append((curr[0],     curr[1],     curr[2] + 1))
    stack.append((curr[0],     curr[1],     curr[2] - 1))

# Get lax envelope
max_x = 0
max_y = 0
max_z = 0
for cube in cubes:
  max_x = max(cube[0], max_x)
  max_y = max(cube[1], max_y)
  max_z = max(cube[2], max_z)
max_x += 3
max_y += 3
max_z += 3

# Add air cubes
for x, y, z in product(range(0, max_x), range(0, max_y), range(0, max_z)):
  cube = (x, y, z)

  # Is already lava
  if cube in cubes:
    continue
  # Mark as neither lava nor air
  cubes[cube] = -1

# Mark corner as air and spread from there
spread_component(cubes, (0, 0, 0), 1)
print(get_uncovered(cubes))
