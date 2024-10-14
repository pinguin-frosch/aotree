from typing import List


class Node:
    id: str = ""
    value: float = 0
    and_nodes: List["Node"] = []
    and_value: float = 0
    or_nodes: List["Node"] = []
    or_value: float = 0

    def __init__(self, id: str, value: float):
        self.id = id
        self.value = value


class Tree:
    nodes: dict[str, Node] = {}

    def __init__(self, nodes: dict[str, float]):
        for id, value in nodes.items():
            node = Node(id, value)
            self.nodes[id] = node

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def print(self):
        for node in self.nodes:
            print(node)
