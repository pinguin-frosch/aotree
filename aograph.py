class Node:
    def __init__(self, id: str, value: float):
        self.id = id
        self.value = value
        self.and_nodes: dict[str, "Node"] = {}
        self.and_value: float = 0
        self.or_nodes: dict[str, "Node"] = {}
        self.or_value: float = 0

    def __str__(self) -> str:
        repr = "{}: value {}, ".format(self.id, self.value)
        repr += "and {{value: {}, nodes: [".format(self.and_value)
        for i, id in enumerate(self.and_nodes):
            repr += "{}".format(id)
            if i != len(self.and_nodes) - 1:
                repr += ", "
        repr += "]}, "
        repr += "or {{value: {}, nodes: [".format(self.or_value)
        for i, id in enumerate(self.or_nodes):
            repr += "{}".format(id)
            if i != len(self.or_nodes) - 1:
                repr += ", "
        repr += "]}"
        return repr


class Tree:
    nodes: dict[str, Node] = {}

    def __init__(self, nodes: dict[str, float]):
        for id, value in nodes.items():
            node = Node(id, value)
            self.nodes[id] = node

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_or_connection(self, parent_id: str, *children_ids: str):
        parent = self.nodes[parent_id]
        for child_id in children_ids:
            child = self.nodes[child_id]
            parent.or_nodes[child_id] = child

    def add_and_connection(self, parent_id: str, *children_ids: str):
        parent = self.nodes[parent_id]
        for child_id in children_ids:
            child = self.nodes[child_id]
            parent.and_nodes[child_id] = child

    def update_cost(self, node_id: str):
        node = self.nodes[node_id]
        if not node.and_nodes and not node.or_nodes:
            return

        for id in node.or_nodes:
            self.update_cost(id)
        for id in node.and_nodes:
            self.update_cost(id)

        costs = []
        if node.and_nodes:
            and_sum = 0
            for _, child in node.and_nodes.items():
                and_sum += child.value + 1
            node.and_value = and_sum
            costs.append(and_sum)
        if node.or_nodes:
            or_sums = []
            for _, child in node.or_nodes.items():
                or_sums.append(child.value + 1)
            node.or_value = min(or_sums)
            costs.append(min(or_sums))

        node.value = min(costs)

    def print(self):
        for _, node in self.nodes.items():
            print(node)
