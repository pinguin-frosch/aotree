import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


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

    def show_shortest_path(self, start):
        graph = nx.DiGraph()

        node_labels = {}
        for id, node in self.nodes.items():
            node_labels[id] = "{}: {}".format(id, node.value)

        for id, node in self.nodes.items():
            if node.and_nodes:
                and_node = "{} {}".format(id, "AND")
                graph.add_node(and_node)
                graph.add_edge(id, and_node, label="{}".format(0.0))
                node_labels[and_node] = "AND: {}".format(node.and_value)
                for child_id in node.and_nodes.keys():
                    graph.add_edge(and_node, child_id, label="{}".format(1.0))
            if node.or_nodes:
                or_node = "{} {}".format(id, "OR")
                graph.add_node(or_node)
                graph.add_edge(id, or_node, label="{}".format(0.0))
                node_labels[or_node] = "OR: {}".format(node.or_value)
                for child_id in node.or_nodes.keys():
                    graph.add_edge(or_node, child_id, label="{}".format(1.0))

        for u, v in graph.edges:
            nx.set_edge_attributes(graph, {(u, v): {"color": "black"}})
        self.highlight_edges(graph, start, "red")

        try:
            pos = graphviz_layout(graph, prog="dot")
        except:
            pos = nx.spring_layout(graph)
            print("Please install GraphViz to use the dot visualization")
            print("Defaulting to the spring layout view")

        edge_colors = [graph[u][v]["color"] for u, v in graph.edges]

        plt.figure(figsize=(8, 6))
        nx.draw(
            graph,
            pos,
            labels=node_labels,
            node_color="skyblue",
            with_labels=True,
            node_size=2000,
            edge_color=edge_colors,
            font_weight="bold",
            font_size=10,
            arrows=True,
        )

        edge_labels = nx.get_edge_attributes(graph, "label")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        plt.title("AND-OR Tree")
        plt.show()

    def print(self):
        for _, node in self.nodes.items():
            print(node)

    def highlight_edges(self, graph: nx.DiGraph, node_id: str, color: str = "blue"):
        node = self.nodes[node_id]
        if not node.and_nodes and not node.or_nodes:
            return

        if node.and_nodes and node.or_nodes:
            if node.and_value < node.or_value:
                self.highlight_and_edges(graph, node, color)
                for id in node.and_nodes:
                    self.highlight_edges(graph, id, color)
            else:
                self.highlight_or_edges(graph, node, color)
                for id in node.or_nodes:
                    self.highlight_edges(graph, id, color)
        elif node.and_nodes and not node.or_nodes:
            self.highlight_and_edges(graph, node, color)
            for id in node.and_nodes:
                self.highlight_edges(graph, id, color)
        else:
            self.highlight_or_edges(graph, node, color)
            for id in node.or_nodes:
                self.highlight_edges(graph, id, color)

    def highlight_and_edges(self, graph: nx.DiGraph, node: Node, color: str = "blue"):
        and_node = "{} {}".format(node.id, "AND")
        node_and_edge = (node.id, and_node)
        nx.set_edge_attributes(graph, {node_and_edge: {"color": color}})
        for id in node.and_nodes:
            and_child_edge = (and_node, id)
            nx.set_edge_attributes(graph, {and_child_edge: {"color": color}})

    def highlight_or_edges(self, graph: nx.DiGraph, node: Node, color: str = "blue"):
        or_node = "{} {}".format(node.id, "OR")
        node_or_edge = (node.id, or_node)
        nx.set_edge_attributes(graph, {node_or_edge: {"color": color}})
        for id, child in node.or_nodes.items():
            if child.value + 1 > node.value:
                continue
            or_child_edge = (or_node, id)
            nx.set_edge_attributes(graph, {or_child_edge: {"color": color}})
            return  # Only use the first one
