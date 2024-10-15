import networkx as nx
import matplotlib.pyplot as plt


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

    def str_children(self) -> str:
        repr = "{"
        and_added = False
        if self.and_nodes:
            and_added = True
            repr += "'AND': ["
            for i, id in enumerate(self.and_nodes):
                repr += "{}".format(id)
                if i != len(self.and_nodes) - 1:
                    repr += ", "
            repr += "]"
        if self.or_nodes:
            if and_added:
                repr += ", "
            repr += "'OR': ["
            for i, id in enumerate(self.or_nodes):
                repr += "{}".format(id)
                if i != len(self.or_nodes) - 1:
                    repr += ", "
            repr += "]"
        repr += "}"
        return repr


class Tree:
    def __init__(self, nodes: dict[str, float]):
        self.nodes: dict[str, Node] = {}
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

        updates = {}
        costs = []
        if node.and_nodes:
            and_sum = 0
            for _, child in node.and_nodes.items():
                and_sum += child.value + 1
            node.and_value = and_sum
            costs.append(and_sum)
            key = " AND ".join(node.and_nodes.keys())
            updates[key] = node.and_value
        if node.or_nodes:
            or_sums = []
            for _, child in node.or_nodes.items():
                or_sums.append(child.value + 1)
            node.or_value = min(or_sums)
            costs.append(min(or_sums))
            key = " OR ".join(node.or_nodes.keys())
            updates[key] = node.or_value

        node.value = min(costs)

        str_children = node.str_children()
        print("{}: {} >>> {}".format(node.id, str_children, updates))

    def show_shortest_path(self):
        graph = nx.DiGraph()

        for id, node in self.nodes.items():
            if node.and_nodes:
                for child_id in node.and_nodes.keys():
                    graph.add_edge(id, child_id, label="AND", color="green")
            if node.or_nodes:
                for child_id in node.or_nodes.keys():
                    graph.add_edge(id, child_id, label="OR", color="blue")

        pos = nx.spring_layout(graph)
        labels = nx.get_edge_attributes(graph, "label")
        colors = [graph[u][v]["color"] for u, v in graph.edges]

        plt.figure(figsize=(8, 6))
        nx.draw(
            graph,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000,
            font_size=10,
            font_weight="bold",
            edge_color=colors,
            arrows=True,
        )
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_color="red")
        plt.title("AND-OR Tree")
        plt.show()

    def print(self):
        for _, node in self.nodes.items():
            print(node)
