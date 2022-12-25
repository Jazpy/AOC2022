with open('inputs/d25.txt', 'r') as in_f:
  lines = [line.strip() for line in in_f.readlines()]

def to_decimal(s):
  digits  = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
  power   = 0
  decimal = 0

  for c in reversed(s):
    decimal += (5 ** power) * digits[c]
    power   += 1

  return decimal

def snafu_carry(ss):
  d_digits = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
  s_digits = {-1: '-', -2: '=', 0: '0', 1: '1', 2: '2', 3: '1=', 4: '1-'}

  carry = 0
  for i, s in enumerate(ss):
    if len(s) == 1 and carry == 0:
      continue

    curr_val  = d_digits[s[1] if len(s) > 1 else s[0]]
    curr_val += carry

    new_s = s_digits[curr_val]

    carry = 0
    if len(s) > 1:
      carry += 1
    if len(new_s) > 1:
      carry += 1
      new_s  = new_s[1]
    ss[i] = new_s

  if carry:
    s.append(s_digits[carry])

def to_snafu(d):
  digits = {0: '0', 1: '1', 2: '2', 3: '1=', 4: '1-'}

  if d == 0:
    return '0'

  snafu = []
  while d > 0:
    d, remainder = divmod(d, 5)
    snafu.append(digits[remainder])

  snafu_carry(snafu)
  snafu.reverse()
  return ''.join(snafu)

# Get fuel in decimal
decimals = []
for line in lines:
  decimals.append(to_decimal(line))
fuel = sum(decimals)

# Print as SNAFU
print(to_snafu(fuel))
