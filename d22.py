import re

with open('inputs/d22.txt', 'r') as in_f:
  lines = [line for line in in_f.readlines()]

class map_row:
  def __init__(self, s):
    self.string = s
    self.left   = len(s) - len(s.lstrip())
    self.right  = len(s.rstrip()) - 1

  def __get_next(self, x, right):
    if x >= self.right and right:
      return self.left
    elif x <= self.left and not right:
      return self.right
    return x + 1 if right else x - 1

  def move_into(self, x):
    valid = x >= self.left and x <= self.right
    return (True, self.string[x]) if valid else (False, None)

  def move(self, start, steps, right):
    curr_x = start
    while steps != 0:
      next_x = self.__get_next(curr_x, right)
      if self.string[next_x] == '#':
        return curr_x
      curr_x = next_x
      steps -= 1

    return curr_x

class cube:
  def __init__(self, raw):
    # Hardcoding everything
    self.faces = []

    # From top left to bottom right
    self.faces.append([row[50:100].strip() for row in raw[:50]])
    self.faces.append([row[100:].strip()   for row in raw[:50]])
    self.faces.append([row[50:100].strip() for row in raw[50:100]])
    self.faces.append([row[0:50].strip()   for row in raw[100:150]])
    self.faces.append([row[50:100].strip() for row in raw[100:150]])
    self.faces.append([row[0:50].strip()   for row in raw[150:200]])

    # Face, facing transitions between cube faces
    self.moving_transitions = {}
    self.moving_transitions[(0, 0)] = (1, 0, False, 0, False)
    self.moving_transitions[(0, 1)] = (2, 1, False, 0, False)
    self.moving_transitions[(0, 2)] = (3, 0, False, 0, True)
    self.moving_transitions[(0, 3)] = (5, 0, True,  0, False)

    self.moving_transitions[(1, 0)] = (4, 2, False, 49, True)
    self.moving_transitions[(1, 1)] = (2, 2, True,  49, False)
    self.moving_transitions[(1, 2)] = (0, 2, False, 49, False)
    self.moving_transitions[(1, 3)] = (5, 3, False, 49, False)

    self.moving_transitions[(2, 0)] = (1, 3, True, 49, False)
    self.moving_transitions[(2, 1)] = (4, 1, False, 0, False)
    self.moving_transitions[(2, 2)] = (3, 1, True, 0, False)
    self.moving_transitions[(2, 3)] = (0, 3, False, 49, False)

    self.moving_transitions[(3, 0)] = (4, 0, False, 0, False)
    self.moving_transitions[(3, 1)] = (5, 1, False, 0, False)
    self.moving_transitions[(3, 2)] = (0, 0, False, 0, True)
    self.moving_transitions[(3, 3)] = (2, 0, True, 0, False)

    self.moving_transitions[(4, 0)] = (1, 2, False, 49, True)
    self.moving_transitions[(4, 1)] = (5, 2, True, 49, False)
    self.moving_transitions[(4, 2)] = (3, 2, False, 49, False)
    self.moving_transitions[(4, 3)] = (2, 3, False, 49, False)

    self.moving_transitions[(5, 0)] = (4, 3, True, 49, False)
    self.moving_transitions[(5, 1)] = (1, 1, False, 0, False)
    self.moving_transitions[(5, 2)] = (0, 1, True, 0, False)
    self.moving_transitions[(5, 3)] = (3, 3, False, 49, False)

    self.pos     = [0, 0]
    self.facing  = 0
    self.face    = 0

  def __get_cell(self, face, pos):
    return self.faces[face][pos[1]][pos[0]]

  def __calculate_score(self):
    chart_pos = self.pos.copy()
    if self.face == 0:
      chart_pos[0] += 50
    elif self.face == 1:
      chart_pos[0] += 100
    elif self.face == 2:
      chart_pos[0] += 50
      chart_pos[1] += 50
    elif self.face == 3:
      chart_pos[1] += 100
    elif self.face == 4:
      chart_pos[0] += 50
      chart_pos[1] += 100
    elif self.face == 5:
      chart_pos[1] += 150

    return 1000 * (chart_pos[1] + 1) + 4 * (chart_pos[0] + 1) + self.facing

  def __get_next(self, face, pos, facing):
    # Going OoB
    if ((facing == 0 and pos[0] + 1 > 49) or
        (facing == 1 and pos[1] + 1 > 49) or
        (facing == 2 and pos[0] - 1 <  0) or
        (facing == 3 and pos[1] - 1 <  0)):
      transition = self.moving_transitions[(face, facing)]
      next_pos   = pos.copy()

      # Reset moving index
      if facing == 0 or facing == 2:
        next_pos[0] = transition[3]

        if transition[4]:
          next_pos[1] = 49 - next_pos[1]
      else:
        next_pos[1] = transition[3]

      # Invert if necessary
      if transition[2]:
        next_pos.reverse()

      return transition[0], next_pos, transition[1]
    # Staying in same face
    else:
      if facing == 0:
        next_pos = [pos[0] + 1, pos[1]]
      if facing == 1:
        next_pos = [pos[0], pos[1] + 1]
      if facing == 2:
        next_pos = [pos[0] - 1, pos[1]]
      if facing == 3:
        next_pos = [pos[0], pos[1] - 1]

      return face, next_pos, facing

  def navigate(self, moves):
    turn_map = {'L': 3, 'R': 1}

    for move in moves:
      # Turn
      if move == 'R' or move == 'L':
        self.facing = (self.facing + turn_map[move]) % 4
        continue
      # Move
      while move != 0:
        next_face, next_pos, next_facing = self.__get_next(
          self.face, self.pos, self.facing)

        if self.__get_cell(next_face, next_pos) == '#':
          break

        self.face   = next_face
        self.pos    = next_pos
        self.facing = next_facing
        move       -= 1

    return self.__calculate_score()

# Parsing
silver_map = []
for line in lines[:-2]:
  silver_map.append(map_row(line))
moves_str = lines[-1]
moves_tok = re.findall('[0-9]+|[L|R]', moves_str)
moves = [int(m) if m != 'L' and m != 'R' else m for m in moves_tok]

gold_cube = cube(lines)

# Silver
def silver(chart):
  turn_map = {'L': 3, 'R': 1}
  pos      = [chart[0].left, 0]
  facing   = 0

  for move in moves:
    # Turn
    if move == 'R' or move == 'L':
      facing = (facing + turn_map[move]) % 4
      continue

    # Move right or left
    if facing == 0 or facing == 2:
      right       = facing == 0
      pos[0] = chart[pos[1]].move(pos[0], move, right)
    # Move down or up
    elif facing == 1 or facing == 3:
      delta_y = 1 if facing == 1 else -1

      while move != 0:
        next_y = (pos[1] + delta_y) % len(chart)
        next_row_valid, cell = chart[next_y].move_into(pos[0])

        # Keep going until we find a valid row, don't count as a move
        while not next_row_valid:
          next_y = (next_y + delta_y) % len(chart)
          next_row_valid, cell = chart[next_y].move_into(pos[0])

        # Stop at wall
        if cell == '#':
          break
        # Valid new row, update position
        pos[1]  = next_y
        move   -= 1

  return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + facing

print(silver(silver_map))

# Gold
print(gold_cube.navigate(moves))
