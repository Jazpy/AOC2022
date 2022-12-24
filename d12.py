import numpy as np
from queue import PriorityQueue

with open('inputs/d12.txt') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

line_ctr   = 0
elevations = []
for line in lines:
  if 'S' in line:
    start_coord = (line_ctr, line.index('S'))
    line        = line.replace('S', 'a')
  if 'E' in line:
    end_coord = (line_ctr, line.index('E'))
    line      = line.replace('E', 'z')

  elevations.append([ord(c) - 96 for c in line])

  line_ctr += 1
elevations = np.array(elevations, dtype=np.int32)

def get_neighbors(curr, elevations, curr_elevation):
  candidates = []
  maxes = elevations.shape
  if curr[0] > 0:
    candidates.append((curr[0] - 1, curr[1]))
  if curr[0] < maxes[0] - 1:
    candidates.append((curr[0] + 1, curr[1]))
  if curr[1] > 0:
    candidates.append((curr[0], curr[1] - 1))
  if curr[1] < maxes[1] - 1:
    candidates.append((curr[0], curr[1] + 1))

  ret = []
  for c in candidates:
    if elevations[c[0]][c[1]] <= curr_elevation + 1:
      ret.append(c)
  return ret

def dijkstra(elevations, starts, end):
  distances = np.full(elevations.shape, np.iinfo(np.int32).max, dtype=np.int32)

  q = PriorityQueue()
  for start in starts:
    distances[start[0]][start[1]] = 0
    q.put((distances[start[0]][start[1]], start))

  while not q.empty():
    curr_n = q.get()
    curr_d = curr_n[0]
    curr_e = elevations[curr_n[1][0]][curr_n[1][1]]

    for coord in get_neighbors(curr_n[1], elevations, curr_e):
      new_d = curr_d + 1

      if new_d < distances[coord[0]][coord[1]]:
        distances[coord[0]][coord[1]] = new_d
        q.put((distances[coord[0]][coord[1]], coord))

  return distances[end[0]][end[1]]

# Silver
print(dijkstra(elevations, [start_coord], end_coord))

# Gold
starts = []
for x in range(elevations.shape[0]):
  for y in range(elevations.shape[1]):
    if elevations[x][y] == 1:
      starts.append((x, y))
print(dijkstra(elevations, starts, end_coord))
