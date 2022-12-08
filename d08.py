import numpy as np

with open('inputs/d08.txt') as in_f:
  lines = in_f.readlines()

tree_heights = np.matrix([[int(c) for c in line.strip()] for line in lines])

def silver_solution(heights):
  visible = np.zeros(heights.shape, dtype=np.int8)
  blocks  = np.full(heights.shape[1], -1, dtype=np.int8)
  for row_h, row_v in zip(heights, visible):
    blocked = np.argwhere(row_h > blocks)[:, 1]
    blocks = np.maximum(blocks, row_h)
    row_v[blocked] = 1

  blocks  = np.full(heights.shape[1], -1, dtype=np.int8)
  for row_h, row_v in zip(heights[::-1], visible[::-1]):
    blocked = np.argwhere(row_h > blocks)[:, 1]
    blocks = np.maximum(blocks, row_h)
    row_v[blocked] = 1

  blocks  = np.full(heights.shape[0], -1, dtype=np.int8)
  for row_h, row_v in zip(heights.T, visible.T):
    blocked = np.argwhere(row_h > blocks)[:, 1]
    blocks = np.maximum(blocks, row_h)
    row_v[blocked] = 1
  blocks  = np.full(heights.shape[0], -1, dtype=np.int8)
  for row_h, row_v in zip(heights.T[::-1], visible.T[::-1]):
    blocked = np.argwhere(row_h > blocks)[:, 1]
    blocks = np.maximum(blocks, row_h)
    row_v[blocked] = 1

  return np.count_nonzero(visible)

def scenic_score(heights, x, y):
  tree_height = heights[x, y]

  # Up
  curr_y   = y - 1
  up_score = 1
  while curr_y >= 0 and heights[x, curr_y] < tree_height:
    up_score += 1
    curr_y   -= 1
  if curr_y < 0:
    up_score -= 1
  # Down
  curr_y     = y + 1
  down_score = 1
  while curr_y < heights.shape[1] and heights[x, curr_y] < tree_height:
    down_score += 1
    curr_y     += 1
  if curr_y == heights.shape[1]:
    down_score -= 1
  # Left
  curr_x     = x - 1
  left_score = 1
  while curr_x >= 0 and heights[curr_x, y] < tree_height:
    left_score += 1
    curr_x     -= 1
  if curr_x < 0:
    left_score -= 1
  # Right
  curr_x      = x + 1
  right_score = 1
  while curr_x < heights.shape[0] and heights[curr_x, y] < tree_height:
    right_score += 1
    curr_x      += 1
  if curr_x == heights.shape[0]:
    right_score -= 1

  return up_score * down_score * left_score * right_score

def gold_solution(heights):
  scenic_scores = np.zeros(heights.shape, dtype=np.int32)
  for x in range(heights.shape[0]):
    for y in range(heights.shape[1]):
      scenic_scores[x, y] = scenic_score(heights, x, y)

  return np.amax(scenic_scores)

# Silver
print(silver_solution(tree_heights))
# Gold
print(gold_solution(tree_heights))
