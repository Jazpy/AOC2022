import re
from collections import defaultdict
from itertools   import product
from functools   import cache

with open('inputs/d16.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

# Build graph
valves    = {}
useful    = []
distances = defaultdict(lambda: defaultdict(lambda: float('inf')))
for line in lines:
  toks = re.split(' |=|;|,', line)

  valve_id   = toks[1]
  valve_flow = int(toks[5])
  valve_adj  = [x for x in toks[11:] if x]
  valves[valve_id] = valve_flow

  # Valve needs opening
  if valve_flow > 0:
    useful.append(valve_id)

  distances[valve_id][valve_id] = 0
  for adj in valve_adj:
    distances[valve_id][adj] = 1

# Find minimum distances from all nodes to each other
for i, j, k in product(valves, repeat=3):
  distances[j][k] = min(distances[j][k], distances[j][i] + distances[i][k])

# DP solution since networkx didn't really work
@cache
def solution(start, time, remaining, gold=False):
  ret = solution('AA', 26, remaining, False) if gold else 0

  for valve in remaining:
    # Time after running and opening
    next_time = time - distances[start][valve] - 1

    if next_time >= 0:
      curr_release  = valves[valve] * next_time
      curr_solution = curr_release + solution(valve, next_time,
        remaining - {valve}, gold)

      # Open valve that maximizes result first
      if curr_solution > ret:
        ret = curr_solution

  return ret

# Silver
print(solution('AA', 30, frozenset(useful)))
# Silver
print(solution('AA', 26, frozenset(useful), True))
