class Node:
    def __init__(self, values):
        self.values = values
        self.left = None
        self.right = None

    def __str__(self):
        return 'Node({values}, {left}, {right})'.format(
            values = self.values,
            left = self.left,
            right = self.right
        )


class Index:
    def __init__(self, indexes):
        self.indexes = indexes
        self.root = None

    def insert(self, values):
        if self.root is None:
            self.root = Node(values)
        else:
            self.__insert(self.root, values)

    def __insert(self, node, values):
        is_equal = True
        for i in self.indexes:
            if node.values[i] == values[i]:
                continue
            is_equal = False
            if node.values[i] > values[i]:
                self.add_node(node, 'left', values)
                break
            else:
                self.add_node(node, 'right', values)
                break
        if is_equal:
            self.add_node(node, 'left', values)

    def add_node(self, node, arg, values):
        new_node = getattr(node,arg)
        if new_node is None:
            setattr(node, arg, Node(values))
        else:
            self.__insert(new_node, values)

    def inorder(self):
        if self.root is None:
            return None
        self.__inorder(self.root)

    def __inorder(self, node):
        if node:
            self.__inorder(node.left)
            print(node.values)
            self.__inorder(node.right)

    def select(self, operator, const):
        values = []
