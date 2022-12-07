with open('inputs/d07.txt') as in_f:
  lines = in_f.readlines()

class Node:
  def __init__(self):
    self.is_leaf = True

    # Files and dirs
    self.files = {}
    self.dirs  = {}

    # Sizes for this dir and all subdirs
    self.s_size = 0
    self.t_size = 0

  def add_dir(self, dir_name):
    self.dirs[dir_name] = Node()
    self.dirs[dir_name].set_par(self)
    self.is_leaf = False

  def add_fil(self, fil_name, fil_size):
    self.files[fil_name] = fil_size
    self.s_size         += fil_size

  def set_par(self, parent):
    self.dirs['..'] = parent

  def set_total_size(self):
    if self.is_leaf:
      self.t_size = self.s_size
      return self.t_size

    acc = self.s_size

    for key, val in self.dirs.items():
      if key == '..':
        continue
      else:
        acc += val.set_total_size()

    self.t_size = acc
    return self.t_size

  def at_most_10k(self, acc):
    new_acc = acc
    for key, val in self.dirs.items():
      if key == '..':
        continue
      else:
        new_acc += val.at_most_10k(acc)

    if self.t_size <= 100000:
      new_acc += self.t_size

    return new_acc

  def smallest_to_free(self, required, candidates):
    if self.t_size >= required:
      candidates.append(self.t_size)

    for key, val in self.dirs.items():
      if key == '..':
        continue
      else:
        val.smallest_to_free(required, candidates)

# Root
root      = Node()
curr_node = root

# Build tree from input
line_idx = 1
while line_idx < len(lines):
  line = lines[line_idx].strip()

  # Parse cd
  if line.startswith('$ cd'):
    dir_name  = line.split()[-1]
    curr_node = curr_node.dirs[dir_name]
    line_idx += 1
  # Parse ls
  else:
    line_idx += 1
    while line_idx < len(lines) and lines[line_idx][0] != '$':
      toks = lines[line_idx].split()

      if toks[0] == 'dir':
        curr_node.add_dir(toks[1])
      else:
        curr_node.add_fil(toks[1], int(toks[0]))

      line_idx += 1

# Set total sizes
free     = 70000000 - root.set_total_size()
required = 30000000 - free

# Silver
print(root.at_most_10k(0))

# Gold
candidate_dirs = []
root.smallest_to_free(required, candidate_dirs)
print(min(candidate_dirs))
