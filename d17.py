from collections import defaultdict

with open('inputs/d17.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]
jets = lines[0]

# Given top left corner, give coordinates used by a rock
def generate_rock_coords(t, coords):
  x, y = coords
  # -
  if t == 0:
    return [[x, y], [x + 1, y], [x + 2, y], [x + 3, y]]
  # +
  if t == 1:
    return [[x + 1, y], [x, y - 1], [x + 1, y - 1],
            [x + 2, y - 1], [x + 1, y - 2]]
  # L
  if t == 2:
    return [[x + 2, y], [x + 2, y - 1],
            [x, y - 2], [x + 1, y - 2], [x + 2, y - 2]]
  # I
  if t == 3:
    return [[x, y], [x, y - 1], [x, y - 2], [x, y - 3]]
  # O
  if t == 4:
    return [[x, y], [x + 1, y], [x, y - 1], [x + 1, y - 1]]

# Get starting top-left coordinates for a rock type given the current max y
def get_start(t, max_y):
  if t == 0:
    return (2, max_y + 4)
  if t == 1 or t == 2:
    return (2, max_y + 6)
  if t == 3:
    return (2, max_y + 7)
  if t == 4:
    return (2, max_y + 5)

# Move a rock if possible given the hole arrangement
def move_rock(rock, hole, move):
  x_move = 1 if move == '>' else -1

  move_possible = True
  for bit in rock:
    if (hole[bit[0] + x_move][bit[1]] == 1 or
        bit[0] + x_move < 0 or bit[0] + x_move > 6):
      move_possible = False
      break

  if move_possible:
    for bit in rock:
      bit[0] += x_move

# Drop a rock if possible, return True if rock has landed
def drop_rock(rock, hole):
  landed = False
  for bit in rock:
    if hole[bit[0]][bit[1] - 1] == 1:
      landed = True
      break

  if not landed:
    for bit in rock:
      bit[1] -= 1

  return landed

# Simulate num_rocks starting with a given type
def simulate(jets, jets_idx, hole, max_y, num_rocks, rock_type):
  # Heights contains max_y after each rock, row_infos contains
  # information to identify rows so we can find cycles
  heights   = []
  row_infos = []

  for _ in range(num_rocks):
    rock      = generate_rock_coords(rock_type, get_start(rock_type, max_y))
    rock_type = (rock_type + 1) % 5

    while True:
      move     = jets[jets_idx]
      jets_idx = (jets_idx + 1) % len(jets)

      # Jet movement
      move_rock(rock, hole, move)
      # Drop movement
      landed = drop_rock(rock, hole)

      if landed:
        # Add to return
        rock_max_y = max(rock, key=lambda x: x[1])[1]
        new_max_y  = max(max_y, rock_max_y)
        heights.append(new_max_y)
        row_infos.append(new_max_y - max_y) # Y delta, corner

        # Set as part of hole
        for bit in rock:
          hole[bit[0]][bit[1]] = 1
        max_y = new_max_y

        # To next rock
        break

  # Return state of simulation to continue if necessary
  return heights, row_infos, jets_idx, max_y, rock_type

def find_cycle(infos, check_len):
  start = infos[:check_len]
  cycle_start = 0
  cycle_end   = 0

  for i in range(0, len(infos) - check_len):
    start = infos[i:i + check_len]
    for j in range(i + check_len, len(infos) - check_len):
      compare = infos[j:j + check_len]

      if start == compare:
        return i, j

# Identify length of rock dropping cycle given input, return list of max_ys
def get_heights(jets):
  ret = []

  # Simulation status init
  hole = defaultdict(lambda: defaultdict(lambda: 0))
  for i in range(7):
    hole[i][0] = 1
  jets_idx  = 0
  max_y     = 0
  rock_type = 0

  # Simulate 10000 rocks
  heights, infos, jets_idx, max_y, rock_type = simulate(jets, jets_idx,
    hole, max_y, 5000, rock_type)

  cycle_start, cycle_end = find_cycle(infos, 16)
  return heights[:cycle_start], heights[cycle_start:cycle_end]

# Get height of stack after dropping num_rocks
def solution(jets, num_rocks):
  start_heights, cycle_heights = get_heights(jets)
  start_stack_height = start_heights[-1] if len(start_heights) else 0

  # Initialize answer with value of stack before entering first cycle
  ret        = start_stack_height
  num_rocks -= len(start_heights)

  # Get max_ys of a bunch of cycles
  full_cycles = num_rocks // len(cycle_heights)
  ret += (cycle_heights[-1] - start_stack_height) * full_cycles

  # And add any leftovers
  remainder   = num_rocks %  len(cycle_heights)
  if remainder > 0:
    ret += cycle_heights[remainder - 1] - start_stack_height

  return ret

# Silver
print(solution(jets, 2022))
# Gold
print(solution(jets, 1000000000000))
