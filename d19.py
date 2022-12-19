import re
from functools import cache

# Parsing
with open('inputs/d19.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]
regex = re.compile('Blueprint (\d+): Each ore robot costs (\d+) ore. '    +
  'Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore ' +
  'and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian')

blueprints = {}
ids        = []
for line in lines:
  dgts = regex.match(line)

  costs     = tuple([int(x) for x in
    [dgts[2], dgts[3], dgts[4], dgts[5], dgts[6], dgts[7]]])
  max_costs = tuple([max(costs[0], costs[1], costs[2], costs[4]),
    costs[3], costs[5]])
  blueprints[int(dgts[1])] = [costs, max_costs]
  ids.append(int(dgts[1]))

def get_available_moves(resources, robots, costs, max_costs):
  # Always pick buying a geode robot if possible
  if resources[0] >= costs[4] and resources[2] >= costs[5]:
    new_resources = (resources[0] - costs[4], resources[1],
      resources[2] - costs[5], resources[3])
    new_robots    = (robots[0], robots[1], robots[2], robots[3] + 1)
    return [(new_resources, new_robots)]

  do_nothing = True
  available_moves = []
  # Buy new obsidian robot
  if (robots[2] < max_costs[2] and
      resources[0] >= costs[2] and resources[1] >= costs[3]):
    new_resources = (resources[0] - costs[2],
      resources[1] - costs[3], resources[2], resources[3])
    new_robots    = (robots[0], robots[1], robots[2] + 1, robots[3])
    available_moves.append((new_resources, new_robots))
    # This heuristic worked for gold but not for silver
    do_nothing = False
  # Buy new ore robot
  if robots[0] < max_costs[0] and resources[0] >= costs[0]:
    new_resources = (resources[0] - costs[0], resources[1],
      resources[2], resources[3])
    new_robots    = (robots[0] + 1, robots[1], robots[2], robots[3])
    available_moves.append((new_resources, new_robots))
    # This heuristic worked for gold but not for silver
    do_nothing = False
  # Buy new clay robot
  if robots[1] < max_costs[1] and resources[0] >= costs[1]:
    new_resources = (resources[0] - costs[1], resources[1],
      resources[2], resources[3])
    new_robots    = (robots[0], robots[1] + 1, robots[2], robots[3])
    available_moves.append((new_resources, new_robots))

  # Do nothing
  if do_nothing:
    available_moves.append((resources, robots))

  return available_moves

@cache
def dfs_search(costs, max_costs, time, resources, robots):
  available_moves = get_available_moves(resources, robots, costs, max_costs)

  if time - 1 == 0:
    return resources[3] + robots[3]

  max_geode = 0
  for move in available_moves:
    prev_res = move[0]
    new_res  = (prev_res[0] + robots[0], prev_res[1] + robots[1],
      prev_res[2] + robots[2], resources[3] + robots[3])
    max_geode = max(max_geode,
      dfs_search(costs, max_costs, time - 1, new_res, move[1]))

  return max_geode

# Setup
start_res = (0, 0, 0, 0)
start_rob = (1, 0, 0, 0)

# Silver
silver = 0
for bp in ids:
  silver += bp * dfs_search(blueprints[bp][0], blueprints[bp][1],
    24, start_res, start_rob)
print(silver)

# Gold
gold = 1
for bp in ids[:3]:
  gold *= dfs_search(blueprints[bp][0], blueprints[bp][1],
    32, start_res, start_rob)
print(gold)
