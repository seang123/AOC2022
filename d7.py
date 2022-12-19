from collections import defaultdict

with open('d7_data.txt', 'r') as f:
    content = f.read().splitlines()


class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

class FolderNode(Node):
    def __init__(self, name, parent, children):
        self.name = name
        self.parent = parent
        self.children = children

    def add_child(self, node: Node):
        node.parent = self
        self.children.append(node)

    def __repr__(self):
        return f'{self.name} -> {self.children}'

class FileNode(Node):
    def __init__(self, name, parent, size):
        self.name = name
        self.parent = parent
        self.size = size

    def __repr__(self):
        return f'{self.name}({self.size})'



def loop(root, content) -> FolderNode:
    current_dir: FolderNode = root
    for line in content:
        cmd = line.strip().split(' ')
        if cmd[0] == '$':
            if cmd[1] == 'cd':
                if cmd[2] == '..':
                    current_dir = current_dir.parent
                else:
                    for node in current_dir.children:
                        if node.name == cmd[2]:
                            current_dir = node
        else:
            if cmd[0] == 'dir':
                new_node = FolderNode(cmd[1], None, [])
                current_dir.add_child(new_node)
            else:
                new_node = FileNode(cmd[1], None, int(cmd[0]))
                current_dir.add_child(new_node)
    return root


def value_of_dir(root, ls: list, limit: int = float('inf')):
    # total of the current folder
    total = 0
    for child in root.children:
        if isinstance(child, FileNode):
            # if a node is a FileNode get its size and add to total
            total += child.size
        elif isinstance(child, FolderNode):
            # if a node is a Folder look into its children and get their size
            size, ls = value_of_dir(child, ls, limit)
            total += size
    if total <= limit:
        ls.append(total)

    return total, ls


def part1():
    root = FolderNode('/', None, [])
    root = loop(root, content)
    total, sizes = value_of_dir(root, [], 100000)
    count = sum([i for i in sizes if i < 100_000])
    print('total:', total)
    print('count:', count)

def part2():
    root = FolderNode('/', None, [])
    root = loop(root, content)
    total, sizes = value_of_dir(root, [])

    min_ = float('inf')
    free = 70_000_000 - total
    need = 30_000_000 - free
    for i in sizes:
        if i >= need:
            if i < min_:
                min_ = i
    print('Smallest to delete:', min_)


part1()
part2()