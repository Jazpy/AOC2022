import re

with open('inputs/d15.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

def manhattan_distance(p0, p1):
  return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])

sensors = []
beacons = []
radii   = []
for line in lines:
  sensor_toks = re.split('=|,', line.split(':')[0])
  beacon_toks = re.split('=|,', line.split(':')[1])
  sensors.append((int(sensor_toks[1]), int(sensor_toks[3])))
  beacons.append((int(beacon_toks[1]), int(beacon_toks[3])))
  radii.append(manhattan_distance(sensors[-1], beacons[-1]))

def silver(sensors, beacons, radii, row):
  marked = set()
  for sensor, radius in zip(sensors, radii):
    to_row = manhattan_distance(sensor, (sensor[0], row))

    # Does not cover row
    if to_row > radius:
      continue

    leftover  = radius - to_row
    leftmost  = sensor[0] - leftover
    rightmost = sensor[0] + leftover

    for x in range(leftmost, rightmost + 1):
      marked.add(x)

  for beacon in beacons:
    if beacon[1] == row:
      marked.discard(beacon[0])

  return len(marked)

def boundary(sensor, radius):
  # Bottom
  y  = sensor[1]
  yd = -1
  for x in range(sensor[0] - radius - 1, sensor[0] + radius + 2):
    yield (x, y)
    if x == sensor[0]:
      yd = 1
    y += yd

  # Top
  y  = sensor[1] + 1
  yd = 1
  for x in range(sensor[0] - radius, sensor[0] + radius + 1):
    yield (x, y)
    if x == sensor[0]:
      yd = -1
    y += yd

def gold(sensors, radii, max_val):
  for sensor, radius in zip(sensors, radii):
    # Target has to be in boundary
    for target in boundary(sensor, radius):
      # Outside specified range
      if (not 0 <= target[0] <= max_val) or (not 0 <= target[1] <= max_val):
        continue

      # If it's within reach of any sensor, go to next candidate
      found = True
      for sensor, radius in zip(sensors, radii):
        if manhattan_distance(sensor, target) <= radius:
          found = False
          break

      if found:
        return target[0] * 4000000 + target[1]

print(silver(sensors, beacons, radii, 2000000))
print(gold(sensors, radii, 4000000))
