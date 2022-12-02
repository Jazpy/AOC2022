with open('inputs/d2.txt') as in_f:
  lines = in_f.readlines()

def score(o, u):
  abc_map = { 'X': 'A', 'Y': 'B', 'Z': 'C' }
  poi_map = { 'A':  1 , 'B':  2 , 'C':  3  }

  if u in 'XYZ':
    u = abc_map[u]

  ret = poi_map[u] + 3

  if ((o == 'A' and u == 'B') or
      (o == 'B' and u == 'C') or
      (o == 'C' and u == 'A')):
    ret += 3
  if ((o == 'A' and u == 'C') or
      (o == 'B' and u == 'A') or
      (o == 'C' and u == 'B')):
    ret -= 3

  return ret

def score_to_win(o, r):
  abc_map = { 'A':  0, 'B':  1, 'C':  2  }
  rep_map = { 'X': -1, 'Y':  0, 'Z':  1  }
  num_map = {  0 : 'A', 1 : 'B', 2 : 'C' }
  o       = abc_map[o]
  u       = max(0, (o + rep_map[r]) % 3)

  return score(num_map[o], num_map[u])

silver_score = 0
gold_score   = 0
for line in lines:
  toks = line.split()
  o = toks[0]
  u = toks[1]

  silver_score += score(o, u)
  gold_score   += score_to_win(o, u)

# Silver star
print(silver_score)
# Gold star
print(gold_score)
