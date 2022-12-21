def get_dir_name(name_stack):
    return '/' + '/'.join(name_stack)

directory_sizes = {'/': 0}

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]

dir_name_stack = []
current_dir_name = '/'

for line in lines[2:]:
    if line == '$ cd ..':
        # When we go up a level we need to add the size of the current directory to parent directory
        parent_dir_name = get_dir_name(dir_name_stack[:-1])
        directory_sizes[parent_dir_name] += directory_sizes[current_dir_name]
        dir_name_stack.pop()
        current_dir_name = get_dir_name(dir_name_stack)
        continue
    if line.startswith('$ cd '):
        dir_name_stack.append(line[5:])
        current_dir_name = get_dir_name(dir_name_stack)
        continue
    if line.startswith('$ ls'):
        directory_sizes[current_dir_name] = 0
        continue
    if line.split(' ')[0].isnumeric():
        directory_sizes[current_dir_name] += int(line.split(' ')[0])

# Now that all the directories are read, propogate the last directory size back up the stack
while len(dir_name_stack) > 0:
    parent_dir_name = get_dir_name(dir_name_stack[:-1])
    directory_sizes[parent_dir_name] += directory_sizes[current_dir_name]
    dir_name_stack.pop()
    current_dir_name = get_dir_name(dir_name_stack)

total = 0
for dir_name, dir_size in directory_sizes.items():
    if dir_size <= 100000:
        total += dir_size

total_space = 70000000
used_space = directory_sizes['/']
needed_space = 30000000 - (total_space - used_space)

candidates = [i for i in directory_sizes.values() if i >= needed_space]
candidates.sort()
print(candidates[0])


